export const Busqueda = {
    props: {
        currentTable: {
            type: String,
            required: true
        },
        currentConnection: {
            type: [String, Number],
            required: true
        }
    },
    template: `
        <div class="acciones d-flex flex-row justify-content-between align-items-center">
            <button type="button" class="btn btn-success btn-lg"><i class="fa-solid fa-play"></i></button>
            <button type="button" class="btn btn-secondary btn-lg">JSON <i class="fa-solid fa-download"></i></button>
            <button type="button" class="btn btn-secondary btn-lg">CSV <i class="fa-solid fa-download"></i></button>
        </div>
        <div class="filtros"></div>
        <div class="resultados"></div>
    `,
    data() {
        return {
            registers: []
        };
    },
    methods: {
    },
    mounted() {
    }
};