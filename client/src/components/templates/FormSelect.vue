<template>
  <fieldset :class="width">
      <div v-if="label" class="block">
          <label
              :for="id"
              class="mb-2 text-sm font-medium text-gray-800"
              :class="labelClass"
          >
              {{ label }}
          </label>
          <span v-if="required && !readonly" class="ml-1 text-red-500">*</span>
      </div>
      <div class="relative items-center" :class="isBlock ? 'flex' : 'inline-flex'">
          <div v-if="hasPrependIcon" class="absolute left-3 text-gray-500">
              <slot name="prepend-icon"></slot>
          </div>
          <div v-if="hasAppendIcon" class="absolute right-3 text-gray-500">
              <slot name="append-icon"></slot>
          </div>
          <div v-if="!readonly" class="relative w-full">
              <button
                  @click="toggleOptions"
                  :id="id"
                  class="border rounded-lg block py-3 h-[40px] flex justify-between items-center"
                  :class="[
                      baseInputStyles,
                      conditionalInputStyles,
                      { 'custom-bg-color': disabled, 'bg-white': !disabled }
                  ]"
                  :disabled="disabled"
              >
                  <div class="text-start truncate">
                      <span v-if="displayValue">{{ displayValue }}</span>
                      <span v-else class="text-gray-400">{{ placeholder }}</span>
                  </div>
                  <!-- <font-awesome-icon :icon="['fas', 'chevron-down']" /> -->
                  <i class="fas fa-chevron-down"></i>
              </button>
              <div
                  v-if="optionsOpen"
                  class="absolute bg-white border shadow-lg w-full z-[9999] rounded-lg max-h-[400px] overflow-auto"
                  :class="optionsPositionClass"
              >
                  <div
                      v-for="(option, index) in options"
                      :key="optionValue ? option[optionValue] : option"
                      class="p-3 h-[40px] cursor-pointer hover:bg-gray-200 flex justify-between items-center"
                      @click="updateValueByList(optionValue ? option[optionValue] : option, optionLabel ? option[optionLabel] : option)"
                      :class="{
                          'rounded-t-lg': index === 0, 
                          'rounded-b-lg': index === options.length - 1
                      }"
                  >
                      {{ optionLabel ? option[optionLabel] : option }}
                  </div>
              </div>
          </div>
          <input
              v-else
              :id="id"
              v-model="displayValue"
              class="block py-3 h-[40px] outline-none"
              :class="[
                  baseInputStyles,
                  conditionalInputStyles
              ]"
              readonly
              :disabled="disabled"
          >
      </div>
      <transition name="shake-fade">
          <small
              v-if="errorMessage"
              class="block text-red-400"
              :class="{ 'opacity-50' : disabled }"
          >
              {{ errorMessage }}
          </small>
      </transition>
  </fieldset>
</template>

<script>
/*
  Example usage:

  <FormSelectComponent
      v-model="selectedOption"
      id="example-select"
      label="Example Label"
      :options="[{ value: 1, label: 'Option 1' }, { value: 2, label: 'Option 2' }]"
      optionValue="value"
      optionLabel="label"
      placeholder="Select an option"
      :required="true"
      :readonly="false"
      :error="hasError"
      :errorMessage="errorMessage"
      :disabled="isDisabled"
      :inputClass="'custom-input-class'"
      :labelClass="'custom-label-class'"
      :isBlock="true"
      @change="handleSelectChange"
  >
      <template #prepend-icon>
          <font-awesome-icon :icon="['fas', 'angle-down']" />
      </template>
      <template #append-icon>
          <font-awesome-icon :icon="['fas', 'check']" />
      </template>
  </FormSelectComponent>
*/
export default {
  name: 'FormSelectComponent',
  emits: ['update:modelValue', 'change'],
  props: {
      modelValue: {
          type: [String, Number, Object, Boolean],
          required: true
      },
      label: {
          type: String,
          required: false
      },
      id: {
          type: String,
          required: true
      },
      placeholder: {
          type: String,
          required: false
      },
      required: {
          type: Boolean,
          default: false
      },
      readonly: {
          type: Boolean,
          default: false
      },
      error: {
          type: Boolean,
          default: false
      },
      errorMessage: {
          type: String,
          default: ''
      },
      disabled: {
          type: Boolean,
          default: false
      },
      inputClass: {
          type: String,
          required: false
      },
      labelClass: {
          type: String,
          required: false
      },
      isBlock: {
          type: Boolean,
          default: true
      },
      width: {
          type: String,
          default: 'w-full'
      },
      options: {
          type: Array,
          default: () => []
      },
      optionValue: {
          type: String,
          default: null
      },
      optionLabel: {
          type: String,
          default: null
      },
      returnObject: {
          type: Boolean,
          default: false
      }
  },
  data() {
      return {
          optionsOpen: false,
          displayValue: '',
          optionsPositionClass: 'mt-1'
      };
  },
  watch: {
      modelValue: {
          immediate: true,
          handler(val) {
              if (this.returnObject && typeof val === 'object') {
                  this.displayValue = val[this.optionLabel];
              } else {
                  const selectedOption = this.options.find(option => option[this.optionValue] === val);
                  this.displayValue = selectedOption ? selectedOption[this.optionLabel] : val;
              }
          }
      }
  },
  computed: {
      hasPrependIcon() {
          return this.$slots['prepend-icon'];
      },
      hasAppendIcon() {
          return this.$slots['append-icon'];
      },
      inputStyles() {
          return [
              this.inputClass,
              this.width,
              {
                  'border-red-300': this.error,
                  'opacity-50 cursor-not-allowed': this.disabled,
                  'pl-10': this.hasPrependIcon,
                  'pr-10': this.hasAppendIcon,
              }
          ];
      },
      baseInputStyles() {
          return [this.inputClass, this.width];
      },
      conditionalInputStyles() {
          return {
              'border-red-300': this.error,
              'opacity-50 cursor-not-allowed': this.disabled,
              'border-b break-words bg-transparent': this.readonly,
              'border rounded-lg px-3': !this.readonly,
              'pl-10': this.hasPrependIcon,
              'pr-10': this.hasAppendIcon,
          };
      }
  },
  methods: {
      toggleOptions(event) {
          this.optionsOpen = !this.optionsOpen;
          if (this.optionsOpen) {
              this.setOptionsPosition(event);
          }
      },
      setOptionsPosition(event) {
          const buttonRect = event.target.getBoundingClientRect();
          const spaceAbove = buttonRect.top;
          const spaceBelow = window.innerHeight - buttonRect.bottom;

          const requiredSpace = this.options.length * 40 + 10;

          if (spaceBelow < requiredSpace && spaceAbove > spaceBelow) {
              this.optionsPositionClass = 'mb-1 bottom-full';
          } else {
              this.optionsPositionClass = 'mt-1';
          }
      },
      updateValueByList(value, label) {
          this.displayValue = label;
          
          const selectedOption = this.options.find(option => 
              this.optionValue ? option[this.optionValue] === value : option === value
          );
          
          this.$emit('update:modelValue', this.returnObject ? selectedOption : value);
          this.$emit('change', this.returnObject ? selectedOption : value);
          this.optionsOpen = false;
      }
  }
}
</script>

<style scoped>
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: none;
}

option {
  background: none;
  color: inherit;
}

.custom-bg-color {
  background-color: light-dark(rgba(239, 239, 239, 0.3), rgba(59, 59, 59, 0.3));
}

.shake-fade-enter-active {
  animation: shake 0.5s ease;
}
.shake-fade-leave-active {
  transition: all 0.5s ease;
}
.shake-fade-enter-from, .shake-fade-leave-to {
  opacity: 0;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
}
</style>
