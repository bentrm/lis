import $ from 'jquery';
import Vue from 'vue/dist/vue.esm';
import './components/AuthorCard';
import './components/Pagination';
import './components/RadioFilter';
import './components/TagFilter';
import './components/Map';


window.$ = $;

import 'popper.js';
import 'bootstrap';
import 'holderjs';
import '@fortawesome/fontawesome-free/js/all'
import Api from './Api';
import {debounce} from './utils';

const api = new Api('/api/v2');

alert("Hello");

// initialize map
const mapOutlet = document.querySelector('#map-outlet');
if (mapOutlet) {
  const mapContainer = new Vue({
    el: mapOutlet,
    template: '#map-container-template',
    data: {
      currentSelection: null,
      memorials: [],
    },
  });

  const memorialList = new Vue({
    el: '#MemorialListContainer',
    template: '#MemorialList',
    delimiters: ["[[", "]]"],
    data: {
      memorials: [],
    },
    methods: {
      selectMemorial: function(memorial) {
        mapContainer.currentSelection = memorial;
      }
    }
  });

  api
    .getMemorials({ limit: 1000 })
    .then(json => {
      mapContainer.memorials = json.results;
      memorialList.memorials = json.results;
  });

  $(window).resize(debounce(setMapHeight, 250));
  setMapHeight();
}

setTimeout(() => {
  $('.SponsorsNav').hide({
    duration: 400
  })             ;
}, 5000);


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

const authorListOutlet = document.querySelector('#authors-list-outlet');
const filterFormOutlet = document.querySelector('#filter-form-outlet');

if (authorListOutlet && filterFormOutlet) {

  const authorList = new Vue({
    el: authorListOutlet,
    template: '#author-card-list-template',
    delimiters: ["[[", "]]"],
    data: {
      filters: {
        limit: 20,
        offset: 0,
      },
      count: 0,
      authors: [],
    },
    computed: {
      currentPage: function() {
        return this.filters.offset / this.limit;
      },
      totalPages: function() {
        return Math.ceil(this.count / this.filters.limit);
      }
    },
    created: function() {
      this.fetchAuthors();
    },
    methods: {
      setPage: function(pageNumber) {
        const newOffset = (pageNumber - 1) * this.filters.limit;
        this.setFilterParam('offset', newOffset);
      },
      setFilterParam: function(param, value) {
        this.filters[param] = value;
        this.fetchAuthors()
      },
      fetchAuthors: function() {
        const vm = this;
        api
          .getAuthors(this.filters)
          .then(json => {
            vm.count = json.count;
            vm.authors = json.results
          });
      }
    },

  });

  new Vue({
    el: filterFormOutlet,
    template: '#filter-form-template',
    delimiters: ["[[", "]]"],
    data: {
      tagFilters: [
        {
          id: 'genre',
          label: 'Genre',
          param: 'genre',
          path: '/genres',
        },
        {
          id: 'language',
          label: 'Languages',
          param: 'language',
          path: '/languages',
        },
        {
          id: 'period',
          label: 'Period',
          param: 'period',
          path: '/periods'
        }
      ],
      genderFilter: {
        id: 'gender',
        label: 'Gender',
        param: 'gender',
        options: [
          {label: 'All', value: '', checked: true},
          {label: 'Female', value: 'F', checked: false},
          {label: 'Male', value: 'M', checked: false},
        ]
      },
    },
    methods: {
      onFilterChange: function (param, value) {
        authorList.setFilterParam(param, value);
      }
    }
  });
}

function setMapHeight() {
  const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
  const sponsorNavHeight = document.querySelector('.SponsorsNav').getBoundingClientRect().height;
  const mainNavHeight = document.querySelector('.MainNav').getBoundingClientRect().height;
  $('.MapView').height(viewportHeight - sponsorNavHeight - mainNavHeight);
}
