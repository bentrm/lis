(function() {
  const paragraphs = document.querySelectorAll(".block-paragraph");
  paragraphs.forEach(p => {
    const anchors = p.querySelectorAll(".footnotes li .footnote-anchor");
    anchors.forEach(anchor => {
      const href = anchor.href;
      if (href) {
        const id = href.split("#")[1];
        if (id) {
          const searchString = `\[${id}\]`;
          const regex = new RegExp(searchString);
        }
      }
    });
  });
}());
