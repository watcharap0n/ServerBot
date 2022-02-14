export const state = () => ({
    data: [],
    response: null,
    dynamicPath: '',
    item: null,
    itemToken: null,
})

export const mutations = {
    setItem(state, payload) {
        state.item = payload
    },
    setItemToken(state, payload) {
        state.itemToken = payload
    },
    payload(state, payload) {
        state.data = payload
    },
    setResponse(state, payload) {
        state.response = payload
    },
    setDynamicPath(state, payload) {
        state.dynamicPath = payload
    }
}

export const actions = {
    async deleteItem(context) {
        const path = context.getters.getDynamicPath;
        this.$axios.delete(path)
            .then((res) => {
                context.commit('setResponse', res.data)
            })
            .catch((err) => {
                context.commit('setResponse', err)
                this.$notifier.showMessage({
                    content: `มีบางอย่างผิดพลาด status code ${err.response.status}`,
                    color: 'red'
                })
            })

    },
    async updateItem(context) {
        const path = context.getters.getDynamicPath;
        await this.$axios.put(path, context.getters.getPayload)
            .then((res) => {
                context.commit('setResponse', res.data)
                this.$notifier.showMessage({
                    content: `แก้ไขแล้ว!`,
                    color: 'success'
                })
            })
            .catch((err) => {
                this.$notifier.showMessage({
                    content: `มีบางอย่างผิดพลาด status code ${err.response.status}`,
                    color: 'red'
                })
            })
    },
    async fetchItem(context) {
        await this.$axios.get(context.getters.getDynamicPath)
            .then((res) => {
                res.data.forEach((v) => {
                    v.id = v._id
                })
                context.commit('setItem', res.data);
            })
            .catch((err) => {
                console.error(err);
            })
    },
    async fetchToken(context) {
        await this.$axios.get(context.getters.getDynamicPath)
            .then((res) => {
                context.commit('setItemToken', res.data.access_token);
            })
            .catch((err) => {
                this.$notifier.showMessage({
                    content: 'มีบางอย่างผิดพลาด',
                    color: 'red'
                })
                console.error(err);
            })
    },
    async fetchCard(context) {
        await this.$axios.get(context.getters.getDynamicPath)
            .then((res) => {
                context.commit('setResponse', res.data)
            })
            .catch((err) => {
                console.error(err);
            })
    }
}


export const getters = {
    getPayload(state) {
        return state.data
    },
    getResponse(state) {
        return state.response
    },
    getDynamicPath(state) {
        return state.dynamicPath
    },
    getItem(state) {
        return state.item
    },
    getToken(state) {
        return state.itemToken
    }
}