export const state = () => ({
    param: '',
    payload: null
})

export const mutations = {
    setParam(state, payload) {
        state.data = payload
    },
    setPayload(state, payload){
        state.payload = payload
    },
    setDefaultRender(state, payload){
        state.payload = payload
        state.param = payload
    }
}

export const actions = {
    async initializedCard(context) {
        const path = `/card?access_token=${context.getters.getParam}`;
        return await this.$axios.get(path)
    },
    async addCard(){
        const path = `/card/create`
        return await this.$axios.post(path)
    },
    async todoCard(context){
        const path = `/card/query/update/${context.getters.getParam}`
        return await this.$axios.put(path, context.getters.getPayload)
    },
    async remove(context){
        const path = `/card/query/delete/${context.getters.getParam}`
        return await this.$axios.delete(path)
    }

}


export const getters = {
    getParam(state) {
        return state.param
    },
    getPayload(state){
        return state.payload
    }
}
