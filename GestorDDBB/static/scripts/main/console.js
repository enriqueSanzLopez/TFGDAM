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
    <h1>Se llega al componente de consola</h1>
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