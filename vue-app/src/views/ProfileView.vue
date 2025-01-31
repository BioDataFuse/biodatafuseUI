<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">Manage your account settings and preferences.</p>
        </div>
        <div class="border-t border-gray-200">
          <dl>
            <!-- Name -->
            <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-500">Full name</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div v-if="!editingName" class="flex justify-between items-center">
                  {{ user.name }}
                  <button
                    @click="startEditName"
                    class="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                  >
                    Edit
                  </button>
                </div>
                <div v-else class="flex items-center space-x-2">
                  <input
                    type="text"
                    v-model="nameEdit"
                    class="flex-1 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  />
                  <button
                    @click="saveName"
                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
                  >
                    Save
                  </button>
                  <button
                    @click="cancelEditName"
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                  >
                    Cancel
                  </button>
                </div>
              </dd>
            </div>

            <!-- Email -->
            <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-500">Email address</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ user.email }}</dd>
            </div>

            <!-- API Key -->
            <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-500">API Key</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div class="flex items-center space-x-2">
                  <input
                    :type="showApiKey ? 'text' : 'password'"
                    v-model="user.apiKey"
                    readonly
                    class="flex-1 shadow-sm block w-full sm:text-sm border-gray-300 rounded-md bg-gray-50"
                  />
                  <button
                    @click="toggleApiKeyVisibility"
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                  >
                    <EyeIcon v-if="!showApiKey" class="h-4 w-4 mr-1" />
                    <EyeSlashIcon v-else class="h-4 w-4 mr-1" />
                    {{ showApiKey ? 'Hide' : 'Show' }}
                  </button>
                  <button
                    @click="regenerateApiKey"
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                  >
                    <ArrowPathIcon class="h-4 w-4 mr-1" />
                    Regenerate
                  </button>
                </div>
              </dd>
            </div>

            <!-- Password -->
            <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-500">Password</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <button
                  @click="showChangePassword = true"
                  class="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                >
                  Change password
                </button>
              </dd>
            </div>

            <!-- Notification Settings -->
            <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-500">Notification preferences</dt>
              <dd class="mt-1 sm:mt-0 sm:col-span-2">
                <div class="space-y-4">
                  <div class="flex items-center">
                    <input
                      id="email-notifications"
                      type="checkbox"
                      v-model="notificationSettings.email"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      @change="saveNotificationSettings"
                    />
                    <label for="email-notifications" class="ml-2 block text-sm text-gray-900">
                      Receive email notifications
                    </label>
                  </div>
                  <div class="flex items-center">
                    <input
                      id="analysis-updates"
                      type="checkbox"
                      v-model="notificationSettings.analysis"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      @change="saveNotificationSettings"
                    />
                    <label for="analysis-updates" class="ml-2 block text-sm text-gray-900">
                      Receive analysis completion updates
                    </label>
                  </div>
                </div>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <TransitionRoot appear :show="showChangePassword" as="template">
      <Dialog as="div" class="relative z-10" @close="showChangePassword = false">
        <TransitionChild
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              enter="ease-out duration-300"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="ease-in duration-200"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  Change Password
                </DialogTitle>

                <form @submit.prevent="handlePasswordChange" class="mt-4 space-y-4">
                  <div>
                    <label for="current-password" class="block text-sm font-medium text-gray-700">
                      Current Password
                    </label>
                    <input
                      type="password"
                      id="current-password"
                      v-model="passwordForm.current"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="new-password" class="block text-sm font-medium text-gray-700">
                      New Password
                    </label>
                    <input
                      type="password"
                      id="new-password"
                      v-model="passwordForm.new"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="confirm-password" class="block text-sm font-medium text-gray-700">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="confirm-password"
                      v-model="passwordForm.confirm"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div class="mt-6 flex justify-end space-x-3">
                    <button
                      type="button"
                      class="inline-flex justify-center rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                      @click="showChangePassword = false"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      :disabled="isPasswordChangeLoading"
                      class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none disabled:opacity-50"
                    >
                      {{ isPasswordChangeLoading ? 'Updating...' : 'Update Password' }}
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { EyeIcon, EyeSlashIcon, ArrowPathIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const user = auth.user

// Name editing
const editingName = ref(false)
const nameEdit = ref(user.name)

function startEditName() {
  nameEdit.value = user.name
  editingName.value = true
}

async function saveName() {
  try {
    await auth.updateProfile({ name: nameEdit.value })
    editingName.value = false
  } catch (error) {
    console.error('Failed to update name:', error)
  }
}

function cancelEditName() {
  editingName.value = false
  nameEdit.value = user.name
}

// API Key handling
const showApiKey = ref(false)

function toggleApiKeyVisibility() {
  showApiKey.value = !showApiKey.value
}

async function regenerateApiKey() {
  try {
    await auth.regenerateApiKey()
  } catch (error) {
    console.error('Failed to regenerate API key:', error)
  }
}

// Password change
const showChangePassword = ref(false)
const isPasswordChangeLoading = ref(false)
const passwordForm = reactive({
  current: '',
  new: '',
  confirm: ''
})

async function handlePasswordChange() {
  if (passwordForm.new !== passwordForm.confirm) {
    alert('New passwords do not match')
    return
  }

  isPasswordChangeLoading.value = true
  try {
    await auth.updatePassword({
      currentPassword: passwordForm.current,
      newPassword: passwordForm.new
    })
    showChangePassword.value = false
    passwordForm.current = ''
    passwordForm.new = ''
    passwordForm.confirm = ''
  } catch (error) {
    console.error('Failed to change password:', error)
  } finally {
    isPasswordChangeLoading.value = false
  }
}

// Notification settings
const notificationSettings = reactive({
  email: user.preferences?.emailNotifications ?? true,
  analysis: user.preferences?.analysisUpdates ?? true
})

async function saveNotificationSettings() {
  try {
    await auth.updateProfile({
      preferences: {
        emailNotifications: notificationSettings.email,
        analysisUpdates: notificationSettings.analysis
      }
    })
  } catch (error) {
    console.error('Failed to update notification settings:', error)
  }
}
</script>