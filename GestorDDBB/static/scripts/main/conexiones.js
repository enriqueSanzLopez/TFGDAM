class ConnectionData{
    constructor(id, token, host, name){
        this.id=id;
        this.token=token;
        this.host=host;
        this.name=name;
    }
};

export const Conexiones = {
    template: `
    <div class="d-flex flex-row justify-content-end align-items-center flex-wrap">
        <button type="button" class="btn btn-light"><i class="fa-solid fa-plug"></i></button>
        <button type="button" class="btn btn-light"><i class="fa-solid fa-plug-circle-xmark"></i></button>
    </div>
    <ul></ul>
    `,
    data() {
        return {
            conexiones: {}
        };
    },
    methods: {
    }
};
