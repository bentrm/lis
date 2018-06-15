"use strict";
$(function() {
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
            node.dataset.toggle = "popover";
            node.dataset.trigger = "hover";
            node.dataset.delay = "500";
            node.dataset.placement = "top";
            node.dataset.html = "true";
            node.innerHTML = "<i class='fas fa-bookmark footnote'></i>";
            quote.replaceWith(node);
            $(node).popover({
              content: footnote.firstChild.innerHTML,
              delay: {show: 500, hide: 1000}
            })
            quoteUsed = true;
          }
        });
      });
      if (quoteUsed) {
        footnote.remove();
      }
    });
  });

  document.querySelectorAll(".block-paragraph .footnotes").forEach(footnotes => {
    console.log(footnotes);
    if (footnotes.querySelector("ol").length === 0) {
      footnotes.remove();
    }
  });
});
