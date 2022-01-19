module.exports = {
    ssr: false,
    head: {
        build: {
            transpile: ['vee-validate'],
            postcss: {
                plugins: {
                    "postcss-custom-properties": false
                },
            },
        },
        titleTemplate: '%s Platform CHATBOT',
        meta: [
            {charset: 'utf-8'},
            {name: 'viewport', content: 'width=device-width, initial-scale=1'},
            {hid: 'description', name: 'description', content: 'Meta description'}
        ],
        script: [
            {
                src: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js'
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
                href: 'https://fonts.googleapis.com/css2?family=Prompt:wght@300&display=swap'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Ubuntu&display=swap'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap'
            }
        ]
    },

    buildModules: [
        "@nuxtjs/vuetify",
        "@nuxtjs/tailwindcss"
    ],

    modules: [
        "@nuxtjs/axios",
        '@nuxtjs/auth-next',
        "bootstrap-vue/nuxt",
        "vue-sweetalert2/nuxt"
    ],


    srcDir: 'app/',

    components: true,

    axios: {
        baseURL: 'https://mangoserverbot.herokuapp.com'
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
    },
    build: {
        postcss: {
            preset: {
                features: {
                    // Fixes: https://github.com/tailwindcss/tailwindcss/issues/1190#issuecomment-546621554
                    "focus-within-pseudo-class": false
                }
            }
        }
    }
}