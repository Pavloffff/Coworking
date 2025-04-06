export interface User {
	user_id?: number
	name: string
	email: string
	tag?: number
	password_hash: string
	password_salt?: string
	avatar_url?: string
}

// export interface LoginResponse {
// 	result: boolean
// }

export interface AddUserResponse {
	method: string
	model: string
	data: User
}
