import { get } from 'svelte/store';  // Importa la función 'get' de Svelte para obtener el estado de la tienda
import { writable } from '../writeable';  // Importa la función 'writable' para crear una tienda de datos
import { api } from '$api';  // Importa el módulo 'api' para realizar llamadas a la API

// Define las interfaces para los objetos Message y Conversation
export interface Message {
    id?: number;
    role: 'user' | 'assistant' | 'system' | 'pending';
    content: string;
}

export interface Conversation {
    id: number;
    messages: Message[];
}

// Define la interfaz para las opciones de mensaje
export interface MessageOpts {
    useStreaming?: boolean;
    documentId?: string;
}

// Define la interfaz para el estado del chat
export interface ChatState {
    error: string;
    loading: boolean;
    activeConversationId: number | null;
    conversations: Conversation[];
}

// Define el estado inicial del chat
const INITIAL_STATE: ChatState = {
    error: '',
    loading: false,
    activeConversationId: null,
    conversations: []
};

// Crea una tienda de datos con el estado inicial
const store = writable<ChatState>(INITIAL_STATE);

// Función para actualizar el estado del chat
const set = (val: Partial<ChatState>) => {
    store.update((state) => ({ ...state, ...val }));
};

// Función para obtener los mensajes de la conversación activa
const getRawMessages = () => {
    const conversation = getActiveConversation();
    if (!conversation) {
        return [];
    }

    return conversation.messages
        .filter((message) => message.role !== 'pending')
        .map((message) => {
            return { role: message.role, content: message.content };
        });
};

// Función para obtener la conversación activa
const getActiveConversation = () => {
    const { conversations, activeConversationId } = get(store);
    if (!activeConversationId) {
        return null;
    }

    return conversations.find((c) => c.id === activeConversationId);
};

// Función para insertar un mensaje en la conversación activa
const insertMessageToActive = (message: Message) => {
    store.update((s) => {
        const conv = s.conversations.find((c) => c.id === s.activeConversationId);
        if (!conv) {
            return;
        }
        conv.messages.push(message);
    });
};

// Función para eliminar un mensaje de la conversación activa
const removeMessageFromActive = (id: number) => {
    store.update((s) => {
        const conv = s.conversations.find((c) => c.id === s.activeConversationId);
        if (!conv) {
            return;
        }
        conv.messages = conv.messages.filter((m) => m.id != id);
    });
};

// Función para enviar una puntuación a la conversación activa
const scoreConversation = async (score: number) => {
    const conversationId = get(store).activeConversationId;

    return api.post(`/scores?conversation_id=${conversationId}`, { score });
};

// Función para obtener las conversaciones de la API
const fetchConversations = async (documentId: number) => {
    const { data } = await api.get<Conversation[]>(`/conversations?pdf_id=${documentId}`);

    if (data.length) {
        set({
            conversations: data,
            activeConversationId: data[0].id
        });
    } else {
        await createConversation(documentId);
    }
};

// Función para crear una nueva conversación en la API
const createConversation = async (documentId: number) => {
    const { data } = await api.post<Conversation>(`/conversations?pdf_id=${documentId}`);

    set({
        activeConversationId: data.id,
        conversations: [data, ...get(store).conversations]
    });

    return data;
};

// Función para establecer la conversación activa por su ID
const setActiveConversationId = (id: number) => {
    set({ activeConversationId: id });
};

// Función para restablecer el estado del chat
const resetAll = () => {
    set(INITIAL_STATE);
};

// Función para restablecer el mensaje de error
const resetError = () => {
    set({ error: '' });
};

// Exporta las funciones y datos para su uso en otros archivos
export {
    store,
    set,
    setActiveConversationId,
    getRawMessages,
    fetchConversations,
    resetAll,
    resetError,
    createConversation,
    getActiveConversation,
    insertMessageToActive,
    removeMessageFromActive,
    scoreConversation
};
