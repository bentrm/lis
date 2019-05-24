$(function() {
  'use strict';

  const $paragraphs = $('section.block');
  const footnoteData = {
    toggle: 'popover',
    trigger: 'hover',
    delay: 500,
    placement: 'top',
    html: true,
  };

  $paragraphs.each(function() {
    const $paragraph = $(this);
    const $texts = $('.rich-text', $paragraph);
    const $footnotes = $('.footnotes [data-tag]', $paragraph);

    $footnotes.each(function() {
      const $footnote = $(this);
      const tag = $footnote.data('tag');

      $texts.each(function() {
        const $text = $(this);

        $('span.footnote', $text).each(function() {
          const $quote = $(this);
          const template = `
            <span class="bookmark fa-layers fa-fw mr-1">
              <i class="fas fa-bookmark footnote"></i>
              <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-5 up-2">${$footnote.index() + 1}</span>
            </span>
          `;
          const $node = $(template);
          const $footnoteContent = $('.rich-text', $footnote);

          if ($quote.text() === tag.toString()) {
            $node.data(footnoteData);
            $node.popover({
              content: $footnoteContent.html(),
              delay: {show: 500, hide: 1000}
            });
            $node.click(function() {
              const $backlink = $('<span class="bookmark-backlink"><i class="fas fa-arrow-up mr-1"></i></span>');
              const prevBackgroundColor = $footnote.css('backgroundColor');

              $backlink.click(function() {
                $('html, body').animate({
                  scrollTop: $node.offset().top - 100
                }, 1000);
                $backlink.remove();
                $footnote.animate({
                  backgroundColor: prevBackgroundColor,
                });
              });
              $('p:first', $footnoteContent).prepend($backlink);
              $('html, body').animate({
                scrollTop: $footnote.offset().top - 100
              }, 1000);
              $footnote.animate({
                backgroundColor: '#eee',
              }, 2000);
            });
            $quote.replaceWith($node);
          }
        });
      });
    });
  });
});
