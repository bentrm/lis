import '@fortawesome/fontawesome-free/js/all';
import 'bootstrap';
import 'holderjs';
import $ from 'jquery';
import 'popper.js';
import Vue from 'vue/dist/vue.esm';
import Api from './Api';
import AuthorListView from './components/AuthorListView.vue';
import MapView from './components/MapView.vue';
import SearchBar from './components/SearchBar.vue';
import {debounce} from './utils';


window.$ = $;

const api = new Api('/api/v2');
new Vue({
  el: '#search-bar-outlet',
  components: {
    SearchBar,
  },
  data: {
    api,
    results: []
  }
});

setTimeout(() => {
  $('.SponsorsNav').hide({
    duration: 400,
    complete: () => $(window).trigger('resize'),
  });
}, 5000);

// initialize map
const mapViewOutlet = document.querySelector('#map-view-outlet');
if (mapViewOutlet) {
  new Vue({
    el: mapViewOutlet,
    components: {
      MapView,
    },
    data: {
      api,
    }
  });

  window.addEventListener("resize", debounce(setMapHeight, 250));
  setMapHeight();
}

const authorListViewOutlet = document.querySelector('#author-list-view-outlet');
if (authorListViewOutlet) {
  new Vue({
    el: authorListViewOutlet,
    components: {
      AuthorListView,
    },
    data: {
      api,
    }
  })
}


const $btns = $('button[data-group="Level"]');
$btns.on('click', e => {
  const $btn = $(e.target);
  const $collapseTarget = $($btn.data('target'));
  const collapseTarget = $collapseTarget.get(0);

  $btns.removeClass('active');
  $btn.addClass('active');

  $('.Level').each((idx, element) => {
    if (element === collapseTarget) {
      $(element).collapse("show");
    } else {
      $(element).collapse("hide");
    }
  })
});

$('.modal').on('show.bs.modal', e => {
  const $rendition = $('.modal-rendition', e.target).get(0);
  $rendition.src = $rendition.dataset.src;
});


// AuthorList interactions
// TODO: refactor
if ($('.AuthorList').get(0)) {
  const $paragraphs = $('section');
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
    const $footnotes = $('.footnotes li[data-tag]', $paragraph);

    $footnotes.each(function() {
      const $footnote = $(this);
      const tag = $footnote.data('tag');

      $texts.each(function() {
        const $text = $(this);

        $('span.footnote', $text).each(function() {
          const $quote = $(this);
          const template = `
            <span class="bookmark fa-layers">
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
              delay: {show: 100, hide: 1000}
            });
            $node.click(function() {
              const $backlink = $('<span class="bookmark-backlink"><i class="fas fa-arrow-up mr-1"></i></span>');
              const prevBackgroundColor = $footnote.css('backgroundColor');

              $backlink.click(function() {
                $('html, body').animate({
                  scrollTop: $node.offset().top - 100
                }, 1000);
                $backlink.remove();
                $footnote.removeClass('active')
              });
              $('p:first', $footnoteContent).prepend($backlink);
              $('html, body').animate({
                scrollTop: $footnote.offset().top - 100
              }, 1000);
              $footnote.addClass('active')
            });
            $quote.replaceWith($node);
          }
        });
      });
    });
  });
}

function setMapHeight() {
  const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
  const sponsorNavHeight = document.querySelector('.SponsorsNav').getBoundingClientRect().height;
  const mainNavHeight = document.querySelector('.MainNav').getBoundingClientRect().height;
  $('.MapView').height(viewportHeight - sponsorNavHeight - mainNavHeight);
}
