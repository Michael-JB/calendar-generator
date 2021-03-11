import argparse
import calendar
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

MONTHS = calendar.month_name[1:]
DAYS = [day[:2] for day in calendar.day_name]


def generate_calendar(year, output_file):
    calendar_document = SimpleDocTemplate(
        output_file,
        pagesize=landscape(A4),
        leftMargin=cm,
        rightMargin=cm,
        topMargin=cm,
        bottomMargin=cm,
    )

    # Format table data
    months = calendar.Calendar().yeardays2calendar(year, width=12)[0]
    formatted_months = [_format_month(month) for month in months]
    transposed_months = [list(row) for row in zip(*formatted_months)]
    table_data = [MONTHS] + transposed_months

    # Create table
    table_style = TableStyle(
        [
            ("FONT", (0, 0), (-1, -1), "Courier", 8),
            ("FONT", (0, 0), (-1, 0), "Courier-Bold", 10, 14),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("ALIGN", (0, 0), (-1, 0), "CENTRE"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
        + [
            ("BACKGROUND", cell, cell, colors.lightgrey)
            for cell in _get_empty_cells(table_data)
        ]
        + [
            ("BACKGROUND", cell, cell, colors.powderblue)
            for cell in _get_day_cells(table_data, 5)
        ]
        + [
            ("BACKGROUND", cell, cell, colors.lightsteelblue)
            for cell in _get_day_cells(table_data, 6)
        ]
    )
    table = Table(
        table_data,
        colWidths=len(MONTHS) * [2.2 * cm],
        rowHeights=[0.75 * cm] + (len(table_data) - 1) * [0.5 * cm],
        style=table_style,
    )

    # Create title
    title_style = ParagraphStyle(
        "titleStyle",
        fontName="Courier-Bold",
        parent=getSampleStyleSheet()["Heading1"],
        alignment=1,
        spaceAfter=0.5 * cm,
    )
    title_text = "Calendar " + str(year)
    title = Paragraph(title_text, title_style)

    calendar_document.title = title_text
    calendar_document.build([title, table])

    print(f"Generated calendar for year {year}. Saved to {output_file}.")


# Given a month as a list of weeks, flattens the list (omitting nil days) and pads to 31
def _format_month(month):
    flat_months = [_day_to_string(day) for week in month for day in week if day[0] != 0]
    return flat_months + [""] * (31 - len(flat_months))


# Returns the locations of all cells matching the given predicate
def _get_cells(table_data, predicate=lambda cell: True):
    return [
        (i, j)
        for j, row in enumerate(table_data)
        for i, cell in enumerate(row)
        if predicate(cell)
    ]


# Returns the locations of all empty cells
def _get_empty_cells(table_data):
    return _get_cells(table_data, lambda cell: len(cell) == 0)


# Returns the locations of all cells housing the given weekday index
def _get_day_cells(table_data, day_index):
    return _get_cells(table_data, lambda cell: DAYS[day_index] in cell)


# Formats a day as a string, padding to length
def _day_to_string(day):
    return "" if day is None else str(day[0]).ljust(2) + " " + DAYS[day[1]]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="the file to which the calendar should be written",
    )
    parser.add_argument(
        "-y",
        "--year",
        help="the year to generate the calendar for",
        type=int,
        default=datetime.now().year,
    )
    args = parser.parse_args()

    generate_calendar(args.year, args.output_file)


if __name__ == "__main__":
    main()
