from memory.long_term_memory import LongTermMemory

long_term_memory = LongTermMemory()


def save_user_details(content):

    for detail in content:

        memory_type = detail["memory_type"]
        details = detail["details"]

        for key, new_content in details.items():

            results = long_term_memory.retrieve_user_details(memory_type)
            updated = False

            for memory in results:
                if (
                    memory["memory_type"] == memory_type
                    and key in memory["details"]
                ):
                    long_term_memory.update_user_details(
                        memory_type,
                        key,
                        new_content
                    )
                    updated = True
                    break

            if not updated:
                long_term_memory.add_user_details([detail])

    return "User memory saved or updated successfully."