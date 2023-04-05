import {SET_HEADER_DATA, SET_ABOUT_PAGE, SET_LOGIN_FORM, SET_CONTACT_FORM} from "../constants/cachePagesConstants";

const initialStore = {
    header: {
        paradoxData: {
            "header": "Парадокс Смита",
            "content": "Хотя вода как ресурс гораздо полезнее кусков кристаллического углерода, называемых нами алмазами, цена последних на международном рынке несоизмеримо выше стоимости воды."
        },
        breadcrumbList: {
            "": [
                {
                    "title": "Главная",
                    "path": null
                }
            ],
            "/about": [
                {
                    "title": "Главная",
                    "path": "/"
                },
                {
                    "title": "О сайте",
                    "path": null
                }
            ],
        }
    },
    aboutPage: "",
    loginForm: [],
    contactForm: []
}

/** Редюсер для заголовка */
export default function cachePageReducer(state = initialStore, action) {
    switch (action.type) {
        case SET_HEADER_DATA:
            return {
                ...state,
                header: {
                    paradoxData: action.paradoxData,
                    breadcrumbList: action.breadcrumbList
                }
            };
        case SET_ABOUT_PAGE:
            return {
                ...state,
                aboutPage: action.html
            }
        case SET_LOGIN_FORM:
            return {
                ...state,
                loginForm: action.form
            }
        case SET_CONTACT_FORM: {
            return {
                ...state,
                contactForm: action.form
            }
        }
        default:
            return state;
    }
}