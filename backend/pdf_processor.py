from PyPDF2 import PdfWriter, PdfReader, Transformation, PageObject


def delete_pages(filename, pages_to_remove):
    '''Delete pages'''
    reader = PdfReader(filename)
    editing_writer = PdfWriter()

    pages_to_remove = set(pages_to_remove)
    total_pages = len(reader.pages)

    for page_num in pages_to_remove:
        if page_num < 0 or page_num >= total_pages:
            raise ValueError(
                f"Invalid page number: {page_num + 1}"
            )

    for delete_index, page in enumerate(reader.pages):

        if delete_index not in pages_to_remove:
            editing_writer.add_page(page)

    filename_edited = filename[:-4] + "_edited.pdf"

    with open(filename_edited, "wb") as f:
        editing_writer.write(f)

    return filename_edited


def add_padding(filename):
    reader = PdfReader(filename)
    padding_writer = PdfWriter()

    with open(filename, "rb") as main_doc:
        padding_writer.append(main_doc)

    PAGES_PER_SHEET = 4
    no_of_pages = len(reader.pages)
    remainder_pages = no_of_pages % PAGES_PER_SHEET

    '''sorting'''

    if (remainder_pages) != 0:

        for _ in range(PAGES_PER_SHEET - remainder_pages):
            padding_writer.add_blank_page(width=padding_writer.pages[0].mediabox.width,
                                          height=padding_writer.pages[0].mediabox.height)

    return padding_writer


def crop_pages(padded_pdf, half_cut):
    crops = []

    for page_edited in padded_pdf.pages:

        new_width = page_edited.mediabox.width
        new_height = page_edited.mediabox.height

        mid = page_edited.mediabox.right / 2
        if half_cut == "left":
            page_edited.mediabox.upper_right = (
                mid,
                page_edited.mediabox.top,
            )
        elif half_cut == "right":
            page_edited.mediabox.lower_left = (
                mid,
                page_edited.mediabox.bottom,
            )

        blank = PageObject.create_blank_page(width=new_width, height=new_height)

        blank.merge_page(page_edited, expand=False)

        crops.append(blank)

    return crops


def merge_crops(crops, half_cut, filename):
    final_writer = PdfWriter()
    for page_index in range(0, len(crops), 2):
        page1 = crops[page_index]
        page2 = crops[page_index + 1]

        if half_cut == "left":
            page2.add_transformation(Transformation().translate(page1.mediabox.width / 2, 0))
            page1.merge_page(page2, expand=False)

            final_writer.add_page(page1)
        elif half_cut == "right":
            page1.add_transformation(Transformation().translate(-(page1.mediabox.width) / 2, 0))
            page2.merge_page(page1, expand=False)

            final_writer.add_page(page2)

    filename_processed = filename[:-4] + "_processed.pdf"

    with open(filename_processed, "wb") as fp:
        final_writer.write(fp)

    return filename_processed


def merge_pdf(filename, half_cut):
    if half_cut not in ("left", "right"):
        raise ValueError(
            "half_cut must be 'left' or 'right'"
        )

    padded_pdf = add_padding(filename)

    cropped_pdf = crop_pages(padded_pdf, half_cut)

    return merge_crops(cropped_pdf, half_cut, filename)
