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
          <input
              :id="id"
              :type="type"
              :placeholder="placeholder"
              :required="required"
              :value="modelValue"
              @input="updateValue($event)"
              @change="onChange($event)"
              class="block py-3 h-[40px] outline-none"
              :class="[
                  baseInputStyles,
                  conditionalInputStyles
              ]"
              :disabled="disabled"
              :readonly="readonly"
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

  <FormInput
      v-model="userInput"
      label="Username"
      id="username-input"
      type="text"
      placeholder="Enter your username"
      :error="hasError"
      :errorMessage="usernameErrorMessage"
      :disabled="isDisabled"
      :readonly="isReadonly"
      :required="true"
      :inputClass="'custom-input-class'"
      :labelClass="'custom-label-class'"
      @change="handleInputChange"
  >
      <template #append-icon>
          <font-awesome-icon :icon="['fas', 'user']" />
      </template>
  </FormInput>
*/
export default {
  name: 'FormInputComponent',
  emits: ['update:modelValue', 'change'],
  props: {
      modelValue: {
          type: [String, Number],
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
      type: {
          type: String,
          default: 'text'
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
      }
  },
  methods: {
      updateValue(event) {
          this.$emit('update:modelValue', event.target.value);
      },
      onChange(event) {
          this.$emit('change', event.target.value);
      }
  },
  computed: {
      hasPrependIcon() {
          return this.$slots['prepend-icon'];
      },
      hasAppendIcon() {
          return this.$slots['append-icon'];
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
              'no-arrows': this.type === 'number'
          };
      },
  }
}
</script>

<style scoped>
.no-arrows::-webkit-outer-spin-button,
.no-arrows::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.no-arrows {
  -moz-appearance: textfield;
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
