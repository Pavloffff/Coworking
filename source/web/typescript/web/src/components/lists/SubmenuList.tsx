import React, { useState } from 'react'
import { Menu, List, Typography, Input, Button } from 'antd'
import {
	PlusOutlined,
	EditOutlined,
	DeleteOutlined,
	CheckOutlined,
} from '@ant-design/icons'

interface SubmenuListProps {
	title: string
	initialItems?: string[]
}

const SubmenuList: React.FC<SubmenuListProps> = ({
	title,
	initialItems = [],
}) => {
	const [items, setItems] = useState<string[]>(initialItems)
	const [newItem, setNewItem] = useState<string>('')
	const [editingIndex, setEditingIndex] = useState<number | null>(null)
	const [editingText, setEditingText] = useState<string>('')

	// Добавление нового элемента
	const addItem = (): void => {
		if (newItem.trim() === '') return
		setItems([...items, newItem])
		setNewItem('')
	}

	// Удаление элемента по индексу
	const deleteItem = (index: number): void => {
		const newItems = [...items]
		newItems.splice(index, 1)
		setItems(newItems)
	}

	// Начало редактирования элемента
	const startEditing = (index: number, item: string): void => {
		setEditingIndex(index)
		setEditingText(item)
	}

	// Сохранение изменений элемента
	const saveEditing = (index: number): void => {
		if (editingText.trim() === '') return
		const newItems = [...items]
		newItems[index] = editingText
		setItems(newItems)
		setEditingIndex(null)
		setEditingText('')
	}

	// Отмена редактирования
	const cancelEditing = (): void => {
		setEditingIndex(null)
		setEditingText('')
	}

	return (
		<Menu mode="inline" style={{ width: 300 }}>
			<Menu.SubMenu key="sub1" title={title}>
				<div style={{ padding: '0 16px' }}>
					{/* Поле ввода для нового элемента */}
					<Input
						placeholder="Введите новый элемент"
						value={newItem}
						onChange={e => setNewItem(e.target.value)}
						onPressEnter={addItem}
						style={{ marginBottom: 8 }}
					/>
					{/* Кнопка добавления */}
					<Button
						type="primary"
						icon={<PlusOutlined />}
						onClick={addItem}
						style={{ marginBottom: 16 }}
					>
						Добавить
					</Button>
					{/* Список элементов */}
					<List
						dataSource={items}
						renderItem={(item, index) => (
							<List.Item
								actions={
									editingIndex === index
										? [
												<Button
													key="save"
													type="link"
													icon={<CheckOutlined />}
													onClick={() => saveEditing(index)}
												/>,
												<Button
													key="cancel"
													type="link"
													onClick={cancelEditing}
												>
													Отмена
												</Button>,
										  ]
										: [
												<Button
													key="edit"
													type="link"
													icon={<EditOutlined />}
													onClick={() => startEditing(index, item)}
												/>,
												<Button
													key="delete"
													type="link"
													icon={<DeleteOutlined />}
													onClick={() => deleteItem(index)}
												/>,
										  ]
								}
							>
								{editingIndex === index ? (
									<Input
										value={editingText}
										onChange={e => setEditingText(e.target.value)}
										onPressEnter={() => saveEditing(index)}
									/>
								) : (
									<Typography.Text>{item}</Typography.Text>
								)}
							</List.Item>
						)}
					/>
				</div>
			</Menu.SubMenu>
		</Menu>
	)
}

export default SubmenuList
