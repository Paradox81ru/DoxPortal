import {SET_HEADER_DATA, SET_ABOUT_PAGE, SET_LOGIN_FORM, SET_CONTACT_FORM} from "../constants/cachePagesConstants";

/** Устанавливает данные заголовка */
function setHeaderDate(data) {
    return {
        type: SET_HEADER_DATA,
        paradoxData: data.paradoxData,
        breadcrumbList: data.breadcrumbList
    }
}

/** Устанавливает данные для страницы "О сайте" */
function setAboutPage(html) {
    return {
        type: SET_ABOUT_PAGE,
        html: html
    }
}

/** Устанавливает данные для формы логировния */
function setLoginForm(form) {
    return {
        type: SET_LOGIN_FORM,
        form: form
    }
}

/** Устанавливает данные для формы обратной связи */
function setContactForm(form) {
    return {
        type: SET_CONTACT_FORM,
        form: form
    }
}

export {setHeaderDate, setAboutPage, setLoginForm, setContactForm};