import { AxiosResponse } from 'axios'
import { ChatItemModel, ChatItemScheme } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const chatItemsApi = {
	getTextChannelsChatItems: async (
		text_channel_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ChatItemScheme[]>> => {
		return handleApiRequest<ChatItemScheme[]>({
			method: 'get',
			url: `chat-items/text-channel?text_channel_id=${text_channel_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	// addChatItem: async (
	// 	chat_item_id: number,
	// 	user_id: number,
	// 	text_channel_id: number,
	// 	text: string | null,
	// 	file: File | null,
	// 	access_token: string,
	// 	refresh_token: string
	// ): Promise<AxiosResponse<ChatItemModel>> => {
	// 	const modelData = {
	// 		chat_item_id: chat_item_id || 0,
	// 		user_id,
	// 		text_channel_id,
	// 		text: text || String(),
	// 		file_url: String(),
	// 	}

	// 	const formData = new FormData()
	// 	formData.append('model', JSON.stringify(modelData))
	// 	// console.log(formData)
	// 	for (const [key, value] of formData.entries()) {
	// 		console.log(`${key}:`, value)
	// 	}

	// 	if (file) {
	// 		formData.append('file', file)
	// 	}

	// 	console.log(JSON.stringify(modelData))

	// 	return handleApiRequest<ChatItemModel>({
	// 		method: 'post',
	// 		url: 'chat-items/add',
	// 		access_token,
	// 		refresh_token,
	// 		data: formData,
	// 		apiClient: serversConfiguratorApiClient,
	// 	})
	// },
	addChatItem: async (
		chat_item_id: number,
		user_id: number,
		text_channel_id: number,
		text: string | null,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ChatItemModel>> => {
		return handleApiRequest<ChatItemModel>({
			method: 'post',
			url: 'chat-items/add',
			data: {
				chat_item_id: chat_item_id || 0,
				user_id,
				text_channel_id,
				text: text || '',
				file_url: '',
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
}
