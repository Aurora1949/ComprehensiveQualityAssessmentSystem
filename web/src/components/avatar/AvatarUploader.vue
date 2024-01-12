<template>
  <div class="p-4">
    <!-- Trigger Button for Modal -->
    <input type="file" ref="fileInput" class="hidden" @change="onSelectFile" />
    <button
      class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
      @click="triggerFileInput"
    >
      上传头像
    </button>

    <!-- Modal Dialog -->
    <TransitionRoot as="template" :show="openModal">
      <Dialog as="div" class="relative z-10" @close="closeModal">
        <!-- Overlay -->
        <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>

        <!-- Modal Panel -->
        <div class="fixed inset-0 z-10 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center sm:items-center sm:p-0">
            <TransitionChild as="div" enter="ease-out duration-300" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100" leave="ease-in duration-200" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95">
              <!-- Modal Content -->
              <DialogPanel class="relative bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div class="sm:flex sm:items-start">
                    <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                      <!-- Modal Header -->
                      <DialogTitle as="h3" class="text-lg leading-6 font-medium text-gray-900">
                        Crop your image
                      </DialogTitle>
                      <div class="mt-2">
                        <!-- Image Crop Area -->
                        <vue-cropper
                          v-if="imageSrc"
                          :src="imageSrc"
                          :aspect-ratio="1"
                          :view-mode="2"
                          @cropend="onCrop"
                          ref="cropper"
                          class="w-full"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Modal Footer -->
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button @click="uploadAvatar" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-500 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
                    Crop Image
                  </button>
                  <button @click="closeModal" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                    Cancel
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script lang="ts">
import { ref, Ref } from 'vue';
import {DialogPanel, DialogDescription, TransitionRoot, TransitionChild, DialogTitle, Dialog } from '@headlessui/vue';
import 'cropperjs/dist/cropper.css';
import { uploadFile } from '@/api/user.ts';
import VueCropper from 'vue-cropperjs';
import Cropper  from 'cropperjs'; // 假设这是正确的类型

export default {
  components: {TransitionRoot, DialogPanel, DialogDescription, TransitionChild, DialogTitle, VueCropper, Dialog},
  setup() {
    const openModal = ref(false);
    const imageSrc: Ref<string | null> = ref(null);
    const croppedImage: Ref<string | null> = ref(null);
    const cropper = ref<Cropper | null>(null);
    const fileInput = ref<HTMLElement | null>(null);

    const closeModal = () => {
      openModal.value = false;
    };

    const onSelectFile = (e: Event) => {
      openModal.value = true
      const target = e.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
          imageSrc.value = e.target!.result as string;
        };
        reader.readAsDataURL(target.files[0]);
      }
    };

    const onCrop = () => {
      if (cropper.value) {
        croppedImage.value = cropper.value.getCroppedCanvas().toDataURL();
      }
    };

    const uploadAvatar = async () => {
      if (croppedImage.value) {
        try {
          const formData = new FormData();
          formData.append('file', dataURItoBlob(croppedImage.value));
          const response = await uploadFile(formData);
          console.log('上传成功', response);
          closeModal();
        } catch (error) {
          console.error('上传失败', error);
        }
      }
    };

    const dataURItoBlob = (dataURI: string) => {
      const byteString = atob(dataURI.split(',')[1]);
      const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(arrayBuffer);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      return new Blob([arrayBuffer], {type: mimeString});
    };

    const triggerFileInput = () => {
      fileInput.value?.click(); // 如果fileInput.value存在，调用它的click()方法
    }

    return {
      openModal,
      imageSrc,
      croppedImage,
      cropper,
      onSelectFile,
      onCrop,
      uploadAvatar,
      closeModal,
      fileInput,
      triggerFileInput,
    };
  }
};
</script>

<style>
/* Tailwind CSS styles */
</style>
