const DYNAMIC = "dynamic";
const IS_MIN = false;

/**
 * Устанавливает динамичные стили
 * @param listStyle {Array} список путей стилей
 */
function setDynamicStyles(listStyle) {
    const head = document.getElementsByTagName("head")[0];
    listStyle.forEach(s => head.append(getLinkStylesheet(s)));
}

/**
 * Формирует элемент link stylesheet
 * @param path путь к файлу таблицей стилей
 * @returns {HTMLLinkElement}
 */
function getLinkStylesheet(path) {
    const ext = IS_MIN ? ".min.css" : ".css";
    let link = document.createElement("link");
    link.setAttribute("data-show", DYNAMIC);
    link.setAttribute("type", "text/css");
    link.setAttribute("href", `/static/${path}${ext}`);
    link.setAttribute("rel", "stylesheet");
    return link;
}

/** Удаляет все динамичные стили */
function clearDynamicStyles() {
    let listStyle = document.querySelectorAll(`head > link[data-show="${DYNAMIC}"]`);
    listStyle.forEach(s => s.remove());
}

export {setDynamicStyles, clearDynamicStyles};