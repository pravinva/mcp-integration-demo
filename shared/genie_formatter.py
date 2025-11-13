"""
Shared Genie response formatter.

Used by both Slack and Teams bots to format Genie MCP responses.
This demonstrates code reuse - same formatting logic for both platforms!
"""

import json


def format_genie_response(raw_response: str, platform: str = "teams") -> str:
    """
    Parse and format Genie's JSON response into human-readable text.

    Genie MCP returns nested JSON: {"content": "{...escaped JSON...}"}
    We need to unpack this double encoding.

    However, Genie can also return:
    - Plain text responses (metadata, table descriptions, help text)
    - Error messages

    Args:
        raw_response: Raw JSON response from Genie MCP
        platform: "slack" or "teams" (affects markdown formatting)

    Returns:
        Formatted human-readable response
    """
    # Debug logging
    print(f"🔍 [FORMATTER] Raw response type: {type(raw_response)}")
    print(f"🔍 [FORMATTER] Raw response length: {len(raw_response) if raw_response else 0}")
    print(f"🔍 [FORMATTER] Raw response first 200 chars: {raw_response[:200] if raw_response else 'None'}")

    try:
        # First parse - outer JSON with "content" field
        outer = json.loads(raw_response)
        print(f"✅ [FORMATTER] Successfully parsed outer JSON")

        # Extract the content field which contains the actual Genie response
        if "content" in outer:
            content_value = outer["content"]

            # Check if content is a JSON string or plain text
            try:
                # Try to parse as JSON (SQL results)
                data = json.loads(content_value)
            except (json.JSONDecodeError, TypeError):
                # Not JSON - it's plain text (metadata, descriptions, etc.)
                # Just return the plain text content
                return content_value.strip()
        else:
            # If no content field, assume it's already the inner data
            data = outer
        
        formatted = []
        
        # Platform-specific markdown formatting
        bold_start = "**" if platform == "teams" else "*"
        bold_end = "**" if platform == "teams" else "*"
        code_block = "```sql" if platform == "teams" else "```"
        
        # Show the SQL query that was generated
        if "query" in data:
            formatted.append(f"📊 {bold_start}SQL Query:{bold_end}\n{code_block}\n{data['query']}\n```\n")
        
        # Extract and format the results
        if "statement_response" in data and "result" in data["statement_response"]:
            result = data["statement_response"]["result"]
            manifest = data["statement_response"]["manifest"]
            
            if "data_array" in result and result["data_array"]:
                # Get column names
                columns = [col["name"] for col in manifest["schema"]["columns"]]
                
                formatted.append(f"{bold_start}Results:{bold_end}\n")
                
                # Format each row
                for row in result["data_array"]:
                    values = row.get("values", [])
                    row_text = []
                    for i, col_name in enumerate(columns):
                        if i < len(values):
                            value = values[i].get("string_value", "N/A")
                            # Format numbers nicely
                            if col_name.lower() in ["total_revenue", "revenue", "amount", "price"]:
                                try:
                                    num_value = float(value)
                                    value = f"${num_value:,.2f}"
                                except (ValueError, TypeError):
                                    pass
                            row_text.append(f"• {bold_start}{col_name}:{bold_end} {value}")
                    formatted.append("\n".join(row_text))
                
                # Add row count
                total_rows = manifest.get("total_row_count", 0)
                formatted.append(f"\n_({total_rows} row{'s' if total_rows != 1 else ''} returned)_")
            else:
                formatted.append("_No results found_")
        
        result_text = "\n".join(formatted)
        
        # Safety check - ensure we return something valid
        if not result_text or result_text.strip() == "":
            return f"Received response but couldn't format it. Raw: {raw_response[:200]}"
        
        return result_text
        
    except json.JSONDecodeError as e:
        # JSON parsing failed - raw_response might be plain text or malformed JSON
        # Try to clean and return it as plain text
        if raw_response and raw_response.strip():
            # Check if it starts with common JSON characters but is malformed
            cleaned = raw_response.strip()
            if cleaned.startswith('{') or cleaned.startswith('['):
                # Looks like JSON but failed to parse - show more detail
                return f"⚠️ Received malformed JSON response:\n\n{cleaned[:500]}"
            else:
                # Not JSON at all - just return the plain text
                return cleaned
        return "Empty response from Genie"
    except Exception as e:
        # If formatting fails, return the original with a note
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Formatter error: {error_details}")

        # Try to return something useful
        if raw_response and raw_response.strip():
            return raw_response.strip()[:500]
        return f"Error formatting response: {str(e)}"


def format_uc_function_response(raw_response: str, platform: str = "teams") -> str:
    """
    Parse and format UC Function JSON response into human-readable text.
    
    UC Functions return JSON with nested structure:
    {"columns": ["output"], "rows": [[{"schema": [...], "values": [...]}]]}
    
    Args:
        raw_response: Raw JSON response from UC Function MCP
        platform: "slack" or "teams" (affects markdown formatting)
    
    Returns:
        Formatted human-readable response
    """
    try:
        data = json.loads(raw_response)
        
        # Platform-specific markdown formatting
        bold_start = "**" if platform == "teams" else "*"
        bold_end = "**" if platform == "teams" else "*"
        
        formatted = [f"{bold_start}Function Result:{bold_end}"]
        
        # UC Functions wrap results in rows -> [0] -> schema + values
        if "rows" in data and len(data["rows"]) > 0:
            # Get the first (and usually only) row
            first_row = data["rows"][0]
            
            if isinstance(first_row, list) and len(first_row) > 0:
                # The actual result is in first_row[0]
                result_obj = first_row[0]
                
                if isinstance(result_obj, dict):
                    # Extract schema and values
                    schema = result_obj.get("schema", [])
                    values = result_obj.get("values", [])
                    
                    # Format each field
                    for i, field_def in enumerate(schema):
                        field_name = field_def.get("name", f"field_{i}")
                        if i < len(values):
                            value = values[i]
                            # Format the value nicely
                            if isinstance(value, (int, float)):
                                # Format numbers nicely
                                if field_name.endswith("percentage") or "percent" in field_name.lower():
                                    formatted.append(f"• {bold_start}{field_name}:{bold_end} {value}%")
                                elif "amount" in field_name.lower() or "discount" in field_name.lower() or "final" in field_name.lower():
                                    formatted.append(f"• {bold_start}{field_name}:{bold_end} ${value:,.2f}")
                                else:
                                    formatted.append(f"• {bold_start}{field_name}:{bold_end} {value:,.2f}")
                            else:
                                formatted.append(f"• {bold_start}{field_name}:{bold_end} {value}")
                    
                    return "\n".join(formatted)
        
        # If we couldn't parse the structure, return a generic success message
        formatted.append("_Function executed successfully_")
        return "\n".join(formatted)
        
    except json.JSONDecodeError as e:
        # Not JSON, return as-is
        return raw_response
    except Exception as e:
        # Show error for debugging
        return f"_Unable to format response: {str(e)}_\n\n```{raw_response[:300]}```"

