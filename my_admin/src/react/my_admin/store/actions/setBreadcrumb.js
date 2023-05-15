import {SET_BREADCRUMB} from "../constans";

/** Устанавливает хлебные крошки */
export default function setBreadcrumb(breadcrumbs) {
    return {
        type: SET_BREADCRUMB,
        breadcrumbList: breadcrumbs
    }

}