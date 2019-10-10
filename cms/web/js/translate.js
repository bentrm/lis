/**
 * Translation strings
 * @type {{}}
 */
const library = {
  'About': {de: 'Über'},
  'Address': {de: 'Adresse'},
  'Admin': {de: 'Admin'},
  'Also known as': {de: 'Auch bekannt als'},
  'Author': {de: 'Autor/in'},
  'Authors': {de: 'Autor/innen'},
  'Back to homepage': {de: 'Zurück zur Startseite'},
  'Biography': {de: 'Biographie'},
  'Born': {de: 'Geboren'},
  'Close': {de: 'Schließen'},
  'Connections': {de: 'Verbindungen'},
  'Content': {de: 'Inhalt'},
  'Dedicated': {de: 'Gewidmet'},
  'Description': {de: 'Beschreibung'},
  'Detailed description': {de: 'Detaillierte Beschreibung'},
  'Died': {de: 'Gestorben'},
  'Directions': {de: 'Wegbeschreibung'},
  'Discover': {de: 'Entdecken'},
  'Error': {de: 'Fehler'},
  'Female': {de: 'Weiblich'},
  'Full texts': {de: 'Volltexte'},
  'Gender': {de: 'Geschlecht'},
  'Genre': {de: 'Genre'},
  'Genres': {de: 'Genres'},
  'Imprint & data protection': {de: 'Impressum & Datenschutz'},
  'Intro': {de: 'Einleitung'},
  'items selected': {de: 'Elemente ausgewählt'},
  'Keyword search': {de: 'Schlagwortsuche'},
  'Keyword search..': {de: 'Schlagwortsuche..'},
  'Keyword..': {de: 'Schlagwort..'},
  'Language': {de: 'Sprache'},
  'Languages': {de: 'Sprachen'},
  'Literary landscape': {de: 'Literaturlandschaft'},
  'Male': {de: 'Männlich'},
  'Map': {de: 'Karte'},
  'Material': {de: 'Material'},
  'Memorial': {de: 'Erinnerungsstelle'},
  'Memorials': {de: 'Erinnerungsstellen'},
  'More': {de: 'Mehr'},
  'Narrow search': {de: 'Suche einschränken'},
  'No filter item available.': {de: 'Kein Schlagwort zur Auswahl.'},
  'No filter item selected.': {de: 'Kein Schlagwort ausgewählt.'},
  'Not found': {de: 'Nicht gefunden'},
  'Periods': {de: 'Epochen'},
  'Primary literature': {de: 'Primärliteratur'},
  'Project partner': {de: 'Projektpartner'},
  'Reception': {de: 'Rezeption'},
  'Research': {de: 'Vertiefen'},
  'Search': {de: 'Suche'},
  'Secondary literature': {de: 'Sekundärliteratur'},
  'See on map': {de: 'Auf der Karte ansehen'},
  'Types': {de: 'Arten'},
  'Works': {de: 'Werk'},
};

/**
 * Currently delivered language. Might be different from browser language.
 */
export const currentLanguage = () => document.documentElement.lang;

const _translate = value => {

  const lang = currentLanguage();

  if (!value) return '';
  value = value.toString().trim();

  if (!library.hasOwnProperty(value)) {
    console.warn('Missing translation:', value);
    return value;
  }

  if (lang !== 'en') {
    if (library[value].hasOwnProperty(lang)) {
      return library[value][lang];
    } else {
      console.warn(`Missing ${lang} translation`, value);
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
