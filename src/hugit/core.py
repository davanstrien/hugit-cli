"""Core code."""

from rich._loop import loop_last
from rich.table import Table

from hugit.console import console


def print_table_from_frequency_dict(frequency_dict: dict, sort_by_value=True):
    """Prints Rich table of dictionary frequencies"""
    if sort_by_value:
        frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1]))
    total = sum(frequency_dict.values())
    table = Table(title="Label Summary")
    table.add_column("Label")
    table.add_column("Count")
    table.add_column("Relative Frequency")
    percents = []
    for last, item in loop_last(frequency_dict.items()):
        label, count = item
        percent = count / total
        percents.append(percent)
        if last:
            table.add_row(label, str(count), f"{percent*100}%", end_section=True)
            table.add_row("Total", str(total), f"{round(sum(percents)*100)}%")
        else:
            table.add_row(label, str(count), f"{round(percent*100,)}%")

    console.print(table)


# def push_dict_to_hub(info: Dict, repo_id: str, path_in_repo: str):
#     token = HfFolder.get_token()
#     info_to_dump = info.copy()
#     buffer = BytesIO()
#     buffer.write(json.dumps(info_to_dump).encode("utf-8"))
#     buffer.write(b"")
#     HfApi().upload_file(
#         path_or_fileobj=buffer.getvalue(),
#         path_in_repo=path_in_repo,
#         repo_id=repo_id,
#         repo_type="dataset",
#         identical_ok=True,
#         token=token,
#     )
