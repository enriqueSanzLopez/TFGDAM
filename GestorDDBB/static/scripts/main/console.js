export const Consola = {
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
        <button type="button" class="btn btn-success btn-lg"><i class="fa-solid fa-search"></i></button>
        <button type="button" class="btn btn-primary btn-lg">JSON <i class="fa-solid fa-download"></i></button>
        <button type="button" class="btn btn-primary btn-lg">CSV <i class="fa-solid fa-download"></i></button>
    </div>
    <textarea v-model="consola" name="codigo" id="codigo" rows="10" class="form-control" placeholder="Código..."></textarea>
    <div class="resultados d-flex flex-column flex-grow-1">
        <p>Resultados</p>
        <div class="result-registers flex-grow-1 overflow-auto"></div>
    </div>
    `,
    data() {
        return {
            registers: [],
            consola: '',
            mostrarFiltros: false,
        };
    },
    methods: {
    },
    mounted() {
    }
};