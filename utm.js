/* Captures UTM params on landing and keeps them for the rest of the session,
   so they're still available on the thank-you page after a beehiiv redirect
   strips the query string. */
(function () {
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  var STORAGE_KEY = 'yfb_utm';

  var params = new URLSearchParams(window.location.search);
  var found = {};
  UTM_KEYS.forEach(function (key) {
    var value = params.get(key);
    if (value) found[key] = value;
  });

  if (Object.keys(found).length > 0) {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(found));
  }

  window.yfbGetUTM = function () {
    try {
      return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}');
    } catch (e) {
      return {};
    }
  };
})();
