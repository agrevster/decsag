import re
from typing import override
from xml.etree.ElementTree import Element
from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import (
    ImageInlineProcessor,
    SimpleTagInlineProcessor,
)
from markdown.treeprocessors import Treeprocessor


class CellClassMarkerProcessor(Treeprocessor):
    def __init__(self, class_markers: dict[str, str]):
        super().__init__()
        self.class_markers: dict[str, str] = {
            k: f"^{v}^" for k, v in class_markers.items()
        }

    @override
    def run(self, root: Element):
        for table in root.iter("table"):
            for row in table.iter("tr"):
                for cell in row:
                    if cell.tag in ["td", "th"]:
                        for class_name, marker in self.class_markers.items():
                            if cell.text and marker in cell.text:
                                cell.text = cell.text.replace(marker, "").strip()
                                existing_class = cell.get("class")
                                if existing_class:
                                    cell.set("class", f"{existing_class} {class_name}")
                                else:
                                    cell.set("class", class_name)


class CellClassExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {"class_markers": [{}, "Dict of markers to class names"]}
        super().__init__(**kwargs)

    @override
    def extendMarkdown(self, md: Markdown):
        md.treeprocessors.register(
            CellClassMarkerProcessor(self.getConfig("class_markers")),
            "cell_class_marker",
            15,
        )


class FigureExtension(Extension):
    @override
    def extendMarkdown(self, md: Markdown):
        FG_RE = r"(-\[)(.+?)(\]-)"
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(FG_RE, "figure"), "figure", 175
        )


class ResizedImagePattern(ImageInlineProcessor):
    @override
    def handleMatch(self, m: re.Match[str], data: str):
        alt_text = m.group(1).strip()
        dimensions = m.group(2).strip()
        src = m.group(3).strip()

        width, height = None, None
        if "x" in dimensions:
            try:
                width, height = dimensions.lower().split("x")
                width = width.strip()
                height = height.strip()
            except ValueError:
                pass

        img = Element("img")
        img.set("src", src)

        img.set("alt", alt_text)

        if width and height:
            img.set("width", width)
            img.set("height", height)

        return img, m.start(0), m.end(0)


class ResizeImageExtension(Extension):
    def extendMarkdown(self, md: Markdown):
        RESIZE_IMG_RE = r"!\[([^\|\]]+)\|([^\]]+)\]\(([^)]+)\)"
        md.inlinePatterns.register(
            ResizedImagePattern(RESIZE_IMG_RE, md), "resizeimage", 175
        )


md = Markdown(
    extensions=[
        CellClassExtension(
            class_markers={
                "bg-critical": "critical",
                "bg-high": "high",
                "bg-medium": "medium",
                "bg-low": "low",
                "bg-info": "info",
                "bg-title": "title",
            }
        ),
        FigureExtension(),
        ResizeImageExtension(),
        "markdown.extensions.tables",
    ]
)


def parse_markdown(text: str) -> str:
    return md.convert(text)
