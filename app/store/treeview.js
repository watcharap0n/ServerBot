export const state = () => ({
    data: [],
    path: '',
})

export const mutations = {
    setTreeview(state, payload) {
        state.data = payload
    },
    setPath(state, payload) {
        state.path = payload
    }
}

export const actions = {
    async initialized(context) {
        if (context.commit('setTreeview')) return;

        const path = context.getters.getPath
        return await this.$axios.get(path)
            .then((res) => {
                res.data.forEach((v) => {
                    v.id = v._id
                })
                context.commit('setTreeview', res.data);
            })
            .catch((err) => {
                console.error(err);
            })
    },
}


export const getters = {
    getInitialized(state) {
        return state.data
    },
    getPath(state) {
        return state.path
    },
}