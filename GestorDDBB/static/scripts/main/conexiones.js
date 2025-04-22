class ConnectionData{
    constructor(id, token, host, table, name){
        this.id=id;
        this.token=token;
        this.host=host;
        this.table=table;
        this.name=name;
    }
};

export const Conexiones = {
    template: `
    <div class="d-flex flex-row justify-content-end align-items-center flex-wrap">
        <button type="button" class="btn btn-light" data-bs-toggle="modal" data-bs-target="#conexion-modal"><i class="fa-solid fa-plug"></i></button>
        <button type="button" class="btn btn-light"><i class="fa-solid fa-plug-circle-xmark"></i></button>
    </div>
    <ul></ul>
    <div class="modal fade" id="conexion-modal" tabindex="-1" aria-labelledby="conexion-modalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <h3 id="create-conexion-modal-title">Conectar</h3>
                    <form>
                        <input type="hidden" name="id" id="id" value="new">
                        <input type="text" id="host" name="host" class="form-control"
                            placeholder="Host...">
                        <select id="tipo" name="tipo" class="form-select form-select-lg"></select>
                        <input type="text" id="database" name="database" class="form-control"
                            placeholder="Base de datos...">
                        <input type="text" id="table" name="table" class="form-control"
                            placeholder="Tabla...">
                        <input type="number" id="port" name="port" class="form-control"
                            placeholder="Puerto...">
                        <input type="text" id="name" name="name" class="form-control"
                            placeholder="Usuario...">
                        <input type="password" id="password" name="passsword" class="form-control"
                            placeholder="Contraseña...">
                        <div class="d-flex flex-row flex-wrap justify-content-end align-items-center">
                            <button type="button" class="btn btn-primary btn-lg">Guardar conexión</button>
                            <button type="button" class="btn btn-secondary btn-lg" data-bs-dismiss="modal">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            conexiones: {}
        };
    },
    methods: {
        async addConnection(){}
    }
};
