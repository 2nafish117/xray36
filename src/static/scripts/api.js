// const http = new XMLHttpRequest()

// http.open("GET", "https://api.lyrics.ovh/v1/toto/africa")
// http.send()

// http.onload = () => console.log(http.responseText)

const xray_base = 'http://localhost:5000/xray/'

var xray = {
    search: {
        get: function (resource, query) {
            return fetch(xray_base + 'search/' + resource + '?' + 'query=' + query)
                .then(
                    res => res.json()
                )
        }
    },

    movies: {
        get: function(id) {
            return fetch(xray_base + 'movies/' + id).then(res => res.json())
        }
    },

    actors: {
        get: function(id) {
            return fetch(xray_base + 'actors/' + id).then(res => res.json())
        }
    },

    shots: {
        get: function(id) {
            console.log(xray_base + 'shots/' + id)
            return fetch(xray_base + 'shots/' + id).then(res => res.json())
        }
    }
}

// /momkKuWburNTqKBF6ez7rvhYVhE.jpg
// https://image.tmdb.org/t/p/original/momkKuWburNTqKBF6ez7rvhYVhE.jpg
const tmdb_key = '73f88711a1bbedabc2a94deef288a168'
const tmdb_profile_root = 'https://image.tmdb.org/t/p/original'
const tmdb_base = 'https://api.themoviedb.org/3/'

// https://image.tmdb.org/t/p/original/kbWValANhZI8rbWZXximXuMN4UN.jpg

var tmdb = {
    get_image: function(path) {
        return fetch(tmdb_profile_root + path)
            .then(
                res => res.json()
            )
    },


}