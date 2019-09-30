/**
 * Translation strings
 * @type {{}}
 */
const library = {
  'Author':    {de: 'Autor/in'},
  'Authors':   {de: 'Autor/innen' },
  'Gender':    {de: 'Geschlecht'},
  'Genre':     {de: 'Genre'},
  'Genres':    {de: 'Genres'},
  'items selected': {de: 'Elemente ausgewählt'},
  'Keyword search': {de: 'Schlagwortsuche'},
  'Keyword..': {de: 'Schlagwort..'},
  'Keyword search..': {de: 'Schlagwortsuche..'},
  'Language':  {de: 'Sprache'},
  'Languages': {de: 'Sprachen'},
  'Memorial':  {de: 'Erinnerungsstelle'},
  'Memorials': {de: 'Erinnerungsstellen'},
  'Narrow search': {de: 'Suche einschränken'},
  'No filter item available.': {de: 'Kein Schlagwort zur Auswahl.'},
  'No filter item selected.': {de: 'Kein Schlagwort ausgewählt.'},
  'Periods':   {de: 'Epochen'},
  'Search':    {de: 'Suche'},
  'Types':     {de: 'Arten'},

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
