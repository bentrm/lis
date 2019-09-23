import {dom, library} from '@fortawesome/fontawesome-svg-core';
import {faBars, faBookmark, faExpandArrowsAlt, faGlobe, faLocationArrow, faSearch, faTimesCircle} from '@fortawesome/free-solid-svg-icons';

// We are only using the user-astronaut icon
library.add(
  faBars,
  faBookmark,
  faExpandArrowsAlt,
  faGlobe,
  faLocationArrow,
  faSearch,
  faTimesCircle,
);

dom.watch();
