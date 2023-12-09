'use strict'
// function camelCase(str) {
//     return str.replace(/-([a-z])/g, (m, s) => s.toUpperCase())
// }

// function hx(attribute, element, defaultValue = null) {
//     if (!element || !element.getAttribute)
//         return null;
//     const value = element.getAttribute('hx-' + attribute) ?? element.dataset(camelCase('hx-' + attribute)) ?? defaultValue
//     return value
// }

HTMLElement.prototype.hx = function(attribute) {
    const defaultValue = {swap: 'innerHTML', trigger: 'click', target: null}
    let attributeValue = this.getAttribute('hx-' + attribute)
    if (attributeValue === null && defaultValue.hasOwnProperty(attribute)) {
        attributeValue = defaultValue[attribute]
    }
    return attributeValue
}

document.addEventListener('click', function (event) {
    //[hx-trigger=click],
    const elem = event.target.closest('[hx-get],[hx-post]')
    if (!elem) return
    const trigger = elem.hx('trigger')
    if (trigger != 'click' && trigger != null) return
    event.preventDefault();
    const fetchOptions = {
        credentials: "same-origin",
        method: elem.hx('post') ? 'POST' : 'GET',
        headers: {
            "HX-Request": true,
            "HX-Current-URL" : document.location.href,
        },
        // body,
    }
    if (elem.hx('prompt')) {
        const value = prompt(elem.hx('prompt'))
        if (value === null) {
            return false;
        }
        fetchOptions.headers["HX-Prompt"] = value;
    }
    if (elem.hx('confirm')) {
        if (!confirm(elem.hx('confirm'))) {
            return false;
        }
    }
    // history.pushState({}, "", url);
    const url = elem.hx('get') ?? elem.hx('post')
    fetch(url, fetchOptions).then(function (response) {
        if (response.headers.get('HX-Redirect')) {
            window.location.href = response.headers.get('HX-Redirect')
            return 'Redirecting...'
        }
        return response.text()
    }).then(function (html) {
        const target = document.querySelector(elem.hx('target')) || (elem.href==url ? document.body : elem)
        switch (elem.hx('swap')) {
            case 'innerHTML':
                target.innerHTML = html
                break
            case 'outerHTML':
                target.outerHTML = html
                break
            case 'afterbegin':
                target.insertAdjacentHTML('afterbegin', html)
                break
            case 'beforebegin':
                target.insertAdjacentHTML('beforebegin', html)
                break
            case 'afterend':
                target.insertAdjacentHTML('afterend', html)
                break
            case 'beforeend':
                target.insertAdjacentHTML('beforeend', html)
                break
            default:
                throw new Error('Unknown swap type: ' + elem.dataset['hxSwap'])
        }
    })
}, false);