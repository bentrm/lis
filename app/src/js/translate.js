import {langHosts} from './config';

const library = {
  'About': { de: 'Über', cs: 'o' },
  'Accessibility': { de: 'Erklärung zur Barrierefreiheit', cs: 'Prohlášení o přístupnosti' },
  'Address': { de: 'Adresse', cs: 'adresa' },
  'Admin': { de: 'Admin', cs: 'admin' },
  'Also known as': { de: 'Auch bekannt als', cs: 'známá také jako' },
  'Author': { de: 'Autor/in', cs: 'autor/autorka' },
  'Authors': { de: 'Autor/innen', cs: 'autoři' },
  'Back to homepage.': { de: 'Zurück zur Startseite.', cs: 'zpět na domovskou stránku' },
  'Biography': { de: 'Biographie', cs: 'biografie' },
  'Born': { de: 'Geboren', cs: 'narozen/narozena' },
  'born': { de: 'geboren', cs: 'narozený' },
  'Close': { de: 'Schließen', cs: 'zavřít' },
  'Contact info': { de: 'Kontaktinformationen', cs: 'kontaktní informace' },
  'Connections': { de: 'Verbindungen', cs: 'spojnice' },
  'Content': { de: 'Inhalt', cs: 'obsah' },
  'Dedicated': { de: 'Gewidmet', cs: 'věnováno' },
  'Description': { de: 'Beschreibung', cs: 'popis' },
  'Detailed description': { de: 'Detaillierte Beschreibung', cs: 'detailní popis' },
  'Died': { de: 'Gestorben', cs: 'zemřel/zemřela' },
  'Directions': { de: 'Wegbeschreibung', cs: 'popis cesty' },
  'Discover': { de: 'Entdecken', cs: 'objevit' },
  'Error': { de: 'Fehler', cs: 'chyba' },
  'Female': { de: 'Weiblich', cs: 'žena' },
  'Filters': { de: 'Filter', cs: 'Filtr' },
  'Full texts': { de: 'Volltexte', cs: 'fulltexty' },
  'Gender': { de: 'Geschlecht', cs: 'rod' },
  'Genre': { de: 'Genre', cs: 'žánr' },
  'Genres': { de: 'Genres', cs: 'žánry' },
  'Home': { de: 'Startseite', cs: 'Domů' },
  'Imprint & data protection': { de: 'Impressum & Datenschutz', cs: 'tiráž' },
  'Intro': { de: 'Einleitung', cs: 'úvod' },
  'items selected': { de: 'Elemente ausgewählt', cs: 'vybrané položky' },
  'Keyword search': { de: 'Schlagwortsuche', cs: 'vyhledávání podle hesel' },
  'Keyword search..': { de: 'Schlagwortsuche..', cs: 'vyhledávání podle hesel' },
  'Keyword..': { de: 'Schlagwort..', cs: 'heslo' },
  'Language': { de: 'Sprache', cs: 'jazyk' },
  'Languages': { de: 'Sprachen', cs: 'jazyky' },
  'Literary landscape': { de: 'Literaturlandschaft', cs: 'literární krajina' },
  'Didactic material': { de: 'Didaktisches Material', cs: 'Didaktický materiál' },
  'Male': { de: 'Männlich', cs: 'muž' },
  'Map': { de: 'Karte', cs: 'mapa' },
  'Material': { de: 'Material', cs: 'materiály' },
  'Memorial': { de: 'Erinnerungsstelle', cs: 'pamětní místo' },
  'Memorials': { de: 'Erinnerungsstellen', cs: 'pamětní místa' },
  'More': { de: 'Mehr', cs: 'více' },
  'Narrow search': { de: 'Suche einschränken', cs: 'vymezit hledání' },
  'No filter item available.': { de: 'Kein Schlagwort zur Auswahl.', cs: 'žádné heslo k výběru' },
  'No filter item selected.': { de: 'Kein Schlagwort ausgewählt.', cs: 'žádé vybrané heslo' },
  'No results..': { de: 'Keine Ergebnisse..', cs: 'žádné výsledky' },
  'Not found': { de: 'Nicht gefunden', cs: 'nenalezeno' },
  'Page not found.': { de: 'Seite nicht gefunden.', cs: 'Stránka nenalezena.'},
  'Periods': { de: 'Epochen', cs: 'epochy' },
  'Please enter a search term..': { de: 'Bitte geben Sie einen Suchbegriff ein..', cs: 'Zadejte hledaný výraz.' },
  'Primary literature': { de: 'Primärliteratur', cs: 'primární literatura' },
  'Project partner': { de: 'Projektpartner', cs: 'projektový partner' },
  'pseudonym': { de: 'Pseudonym', 'cs': 'pseudonym' },
  'Reception': { de: 'Rezeption', cs: 'recepce' },
  'References': { de: 'Einzelnachweise', cs: 'Poznámky pod čarou' },
  'Research': { de: 'Vertiefen', cs: 'prohloubit' },
  'Search term..': { de: 'Suchbegriff..', cs: 'klíčových slov' },
  'Search': { de: 'Suche', cs: 'hledání' },
  'Secondary literature': { de: 'Sekundärliteratur', cs: 'sekundární literatura' },
  'See on map': { de: 'Auf der Karte ansehen', cs: 'zobrazit na mapě' },
  'Testimony': { de: 'Zeugnisse', cs: 'Svědectví' },
  'Types': { de: 'Arten', cs: 'typy' },
  'Works': { de: 'Werk', cs: 'díla' },
  'Zoom to feature extent': { de: 'Auf gesamte Ausbreitung zoomen', cs: 'Přibližte rozsah funkce' },
};

export const availableLanguages = Object.freeze({
  en: 'English',
  de: 'Deutsch',
  cs: 'Česky',
});

/**
 * Currently delivered language. Might be different from browser language.
 * Preconfigured host-specific settings are favoured if no user setting is provided.
 */
export const getCurrentLanguage = () => {
  const cookies = document.cookie;
  const dict = cookies.split(';').reduce((acc, cur) => {
    const [key, value] = cur.trim().split('=');
    acc[key] = value;
    return acc;
  }, {});

  if (dict.lang) {
    return dict.lang;
  }

  const hostname = window.location.hostname;
  const predefinedLang = langHosts[hostname];
  if (predefinedLang) {
    return predefinedLang;
  }

  return 'en';
};

export const setCurrentLanguage = lang => {
  if (availableLanguages[lang]) {
    document.cookie = `lang=${lang}; path=/`;
  }
};

const _translate = value => {

  if (!value) return '';
  value = value.toString().trim();

  if (!library.hasOwnProperty(value)) {
    console.warn('Missing translation:', value);
    return value;
  }

  if (getCurrentLanguage() !== 'en') {
    if (library[value].hasOwnProperty(getCurrentLanguage())) {
      return library[value][getCurrentLanguage()];
    } else {
      console.warn(`Missing ${getCurrentLanguage()} translation`, value);
    }
  }

  return value;
};

const cache = {};
export default value => {
  if (!cache.hasOwnProperty(value)) {
    cache[value] = _translate(value);
  }
  return cache[value];
}
