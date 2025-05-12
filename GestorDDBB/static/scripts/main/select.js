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
            <button type="button" class="btn btn-secondary btn-lg" @click="toggleFiltros"><i class="fa-solid fa-filter"></i></button>
            <button type="button" class="btn btn-secondary btn-lg">JSON <i class="fa-solid fa-download"></i></button>
            <button type="button" class="btn btn-secondary btn-lg">CSV <i class="fa-solid fa-download"></i></button>
        </div>
        <transition @enter="enter"
            @leave="leave">
            <div class="filtros mb-3" v-show="mostrarFiltros">
                <label>Columnas</label>
                <input type="text" class="form-control" v-model="columnas" placeholder="Columnas...">
                <label>Filtros</label>
                <input type="text" class="form-control" v-model="filtros" placeholder="Filtros...">
                <label>Orden</label>
                <input type="text" class="form-control" v-model="orden" placeholder="Orden...">
            </div>
        </transition>
        <div class="resultados d-flex flex-column flex-grow-1">
            <p>Resultados</p>
            <div class="result-registers flex-grow-1"></div>
        </div>
    `,
    data() {
        return {
            registers: [],
            columnas: '*',
            filtros: '',
            orden: '',
            mostrarFiltros: false,
        };
    },
    methods: {
        async toggleFiltros() {
            this.mostrarFiltros = !this.mostrarFiltros;
        },
        enter(el) {
            el.style.boxSizing = 'border-box';
            el.style.overflow = 'hidden';
            el.style.height = '0';
            el.style.opacity = '0';
            el.offsetHeight; // trigger reflow

            const height = el.scrollHeight + 'px';
            el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
            el.style.height = height;
            el.style.opacity = '1';

            // Limpieza al terminar
            el.addEventListener('transitionend', function handler() {
                el.style.height = 'auto';
                el.style.overflow = '';
                el.removeEventListener('transitionend', handler);
            });
        },

        leave(el) {
            el.style.boxSizing = 'border-box';
            el.style.height = el.scrollHeight + 'px';
            el.style.opacity = '1';
            el.offsetHeight; // trigger reflow

            el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
            el.style.height = '0';
            el.style.opacity = '0';
            el.style.overflow = 'hidden';
        }
    },
    mounted() {
    }
};