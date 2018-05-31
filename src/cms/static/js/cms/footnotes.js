(function() {
  const paragraphs = document.querySelectorAll(".block-paragraph");
  paragraphs.forEach(p => {
    const texts = p.querySelectorAll(".rich-text");
    const footnotes = document.querySelectorAll(".footnotes [data-tag]")
    footnotes.forEach(footnote => {
      const tag = footnote.dataset.tag;
      let quoteUsed = false;
      texts.forEach(text => {
        text.querySelectorAll("span.footnote").forEach(quote => {
          if (quote.textContent === tag) {
            const node = document.createElement("span");
            node.classList.add("bookmark", "mx-1");
            node.dataset.toggle = "tooltip";
            node.dataset.placement = "top";
            node.dataset.html = "true";
            node.title = footnote.firstChild.innerHTML;
            node.innerHTML = "<i class='far fa-bookmark footnote'></i>";
            quote.replaceWith(node);
            quoteUsed = true;
          }
        });
      });
      if (quoteUsed) {
        footnote.remove();
      }
    });
  });
  $('[title][data-toggle]').tooltip()
}());
