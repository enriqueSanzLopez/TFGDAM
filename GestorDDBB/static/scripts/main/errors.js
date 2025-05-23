export const ErrorList = {
    props: {
        errors: {
            type: Array,
            default: () => []
        }
    },
    template: `
    <div 
      v-if="errors.length" 
      class="error-list position-fixed bg-white border rounded p-2 shadow-sm"
      >
      <div 
        v-for="error in errors" 
        :key="error.id" 
        class="d-flex justify-content-between align-items-center mb-2"
      >
        <div class="error-message text-break">{{ error.error }}</div>
        <button 
          type="button" 
          class="btn btn-sm btn-danger ms-2" 
          @click="eliminarError(error.id)" 
          aria-label="Eliminar error"
          title="Eliminar error"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
  `,
    methods: {
        async eliminarError(id) {
            const nuevosErrores = this.errors.filter(e => e.id !== id);
            this.$emit('update:errors', nuevosErrores);
        },
    },
    mounted() {
    }
};
