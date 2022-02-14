module.exports = {
    env: {
        branch: process.env.BRANCH || 'review',
        baseUrl: process.env.BASE_URL || 'http://localhost:8500'
    },
    ssr: false,
    head: {
        titleTemplate: '%s Platform CHATBOT',
        meta: [
            {charset: 'utf-8'},
            {name: 'viewport', content: 'width=device-width, initial-scale=1'},
            {hid: 'description', name: 'description', content: 'Meta description'}
        ],
        script: [
            {
                src: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js'
            },
            {
                src: 'http://localhost:8098'
            }
        ],
        link: [
            {
                rel: 'preconnect',
                href: 'https://fonts.googleapis.com'
            },
            {
                rel: 'preconnect',
                href: 'https://fonts.gstatic.com'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Prompt:wght@500&display=swap'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Ubuntu&display=swap'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Kanit:ital,wght@1,300&family=Sarabun:wght@300&display=swap'
            }
        ]
    },
    plugins: [
        '~/plugins/notifier.js'
    ],
    buildModules: [
        "@nuxtjs/vuetify",
        "@nuxtjs/tailwindcss"
    ],

    modules: [
        "@nuxtjs/axios",
        '@nuxtjs/auth-next',
        "bootstrap-vue/nuxt",
        "vue-sweetalert2/nuxt",
        "nuxt-clipboard",
    ],
    srcDir: 'app/',

    components: true,

    axios: {
        baseURL: 'http://localhost:8500'
    },

    clipboard: {
        autoSetContainer: true
    },
    auth: {
        strategies: {
            local: {
                token: {
                    property: 'access_token',
                    global: true,
                    // required: true,
                    type: 'Bearer'
                },
                user: {
                    property: 'data',
                    autoFetch: true
                },
                endpoints: {
                    login: {url: '/authentication/token', method: 'post'},
                    user: {url: '/authentication/user', method: 'get'},
                    logout: {url: '/authentication/logout', method: 'delete'}
                }
            }
        }
    }
}