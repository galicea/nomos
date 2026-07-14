import React, { useState, useRef, useEffect } from 'react'
import axios, { CancelTokenSource } from 'axios'
import { Send, Bot, User, Trash2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Navbar } from '@/components/Navbar'
import { Footer } from '@/components/Footer'
import CONFIG from '@/configs/config'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
  isStreaming?: boolean
}

export default function Index() {
  const apiEndpoint = CONFIG.apiUrl + 'query'
  const welcomeMessage = 'Witaj w Asystencie Nomos. Zadaj mi pytanie projektowanej konstytucji.'

  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const cancelTokenSourceRef = useRef<CancelTokenSource | null>(null)

  // Initialize with welcome message on mount
  useEffect(() => {
    setMessages([
      {
        id: '1',
        text: welcomeMessage,
        sender: 'bot',
        timestamp: new Date(),
      },
    ])
  }, [])

  // Auto-scroll on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Focus input
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleLinkClick = async (path: string) => {
    const botMessageId = Date.now().toString()
    setMessages(prev => [...prev, {
      id: botMessageId,
      text: '',
      sender: 'bot',
      timestamp: new Date(),
      isStreaming: true
    }])

    try {
      const api = axios.create()
      const cleanEndpoint = apiEndpoint.replace('/query', '')
      const response = await api.get(cleanEndpoint + path)
      streamResponse(botMessageId, response.data.response || 'Brak danych.')
    } catch {
      setMessages(prev => prev.map(m =>
        m.id === botMessageId
          ? { ...m, text: 'Błąd ładowania oferty.', isStreaming: false }
          : m
      ))
    }
  }

  const streamResponse = (messageId: string, fullText: string) => {
    setStreamingMessageId(messageId)
    const words = fullText.split(' ')
    let currentText = ''
    let wordIndex = 0

    const streamInterval = setInterval(() => {
      if (wordIndex < words.length) {
        currentText += (wordIndex > 0 ? ' ' : '') + words[wordIndex]
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === messageId ? { ...msg, text: currentText, isStreaming: true } : msg,
          ),
        )
        wordIndex++
      } else {
        clearInterval(streamInterval)
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === messageId ? { ...msg, isStreaming: false } : msg,
          ),
        )
        setStreamingMessageId(null)
      }
    }, 40)
  }

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const userInput = inputText
    setInputText('')
    setIsLoading(true)

    try {
      cancelTokenSourceRef.current = axios.CancelToken.source()
      const botMessageId = (Date.now() + 1).toString()
      const botMessage: Message = {
        id: botMessageId,
        text: '',
        sender: 'bot',
        timestamp: new Date(),
        isStreaming: true,
      }

      setMessages((prev) => [...prev, botMessage])

      const response = await axios.post(
        apiEndpoint,
        {
          message: userInput,
          conversation_history: messages.map((m) => ({
            role: m.sender,
            content: m.text,
          })),
        },
        {
          cancelToken: cancelTokenSourceRef.current.token,
          headers: {
            'Content-Type': 'application/json',
          },
        },
      )

      await new Promise((resolve) => setTimeout(resolve, 300))

      streamResponse(
        botMessageId,
        response.data.response ||
        response.data.message ||
        'Przepraszam, nie otrzymałem odpowiedzi.',
      )
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Request canceled')
      } else {
        console.error('Error sending message:', error)
        const errorMessage: Message = {
          id: Date.now().toString(),
          text: 'Przepraszam, wystąpił błąd. Spróbuj ponownie.',
          sender: 'bot',
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, errorMessage])
      }
    } finally {
      setIsLoading(false)
      cancelTokenSourceRef.current = null
    }
  }

  const handleCancelRequest = () => {
    if (cancelTokenSourceRef.current) {
      cancelTokenSourceRef.current.cancel('Request canceled by user')
      setIsLoading(false)
      if (streamingMessageId) {
        setMessages((prev) => prev.filter((msg) => msg.id !== streamingMessageId))
        setStreamingMessageId(null)
      }
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const clearChat = () => {
    setMessages([
      {
        id: '1',
        text: welcomeMessage,
        sender: 'bot',
        timestamp: new Date(),
      },
    ])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-card to-background flex flex-col">
      <Navbar />

      {/* Main chat section */}
      <main className="flex-1 container mx-auto px-4 pt-24 pb-12 flex flex-col items-center justify-center">
        <div className="w-full max-w-4xl bg-card/60 backdrop-blur-xl border border-border/80 rounded-2xl shadow-lg overflow-hidden flex flex-col h-[calc(100vh-14rem)] min-h-[500px]">

          {/* Header */}
          <div className="p-4 border-b border-border/80 flex items-center justify-between bg-card/40">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary/10 text-primary rounded-xl">
                <Bot size={24} />
              </div>
              <div>
                <h1 className="font-semibold text-lg tracking-tight text-foreground">Asystent Nomos</h1>
                <div className="flex items-center space-x-1.5">
                  <span className="relative flex h-2 w-2">
                    <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isLoading ? 'bg-yellow-400' : 'bg-green-400'}`}></span>
                    <span className={`relative inline-flex rounded-full h-2 w-2 ${isLoading ? 'bg-yellow-500' : 'bg-green-500'}`}></span>
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {isLoading ? 'Generowanie odpowiedzi...' : 'Aktywny'}
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={clearChat}
              className="p-2 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-lg transition-all"
              title="Wyczyść konwersację"
            >
              <Trash2 size={18} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-background/30 scrollbar-thin scrollbar-thumb-border">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
              >
                <div
                  className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 shadow-sm border ${message.sender === 'user'
                    ? 'bg-primary text-primary-foreground border-primary/20 rounded-br-none'
                    : 'bg-card/90 text-foreground border-border/60 rounded-bl-none'
                    }`}
                >
                  <div className="flex items-start space-x-3">
                    {message.sender === 'bot' && (
                      <div className="mt-0.5 flex-shrink-0 p-1 bg-primary/10 text-primary rounded-lg">
                        <Bot size={16} />
                      </div>
                    )}
                    <div className="flex-1 overflow-hidden">
                      <div className="text-sm prose dark:prose-invert max-w-none break-words">
                        <ReactMarkdown
                          components={{
                            a: ({ href, children }) => (
                              <button
                                onClick={() => href && handleLinkClick(href)}
                                className="text-primary underline hover:opacity-80 cursor-pointer font-medium"
                              >
                                {children}
                              </button>
                            ),
                            strong: ({ children }) => (
                              <strong className="font-semibold">{children}</strong>
                            ),
                            ul: ({ children }) => (
                              <ul className="list-disc list-inside mt-1 space-y-1">{children}</ul>
                            ),
                            ol: ({ children }) => (
                              <ol className="list-decimal list-inside mt-1 space-y-1">{children}</ol>
                            ),
                            p: ({ children }) => (
                              <p className="mb-1 last:mb-0 leading-relaxed">{children}</p>
                            ),
                          }}
                        >
                          {message.text}
                        </ReactMarkdown>
                        {message.isStreaming && (
                          <span className="inline-block w-1.5 h-4 ml-1 bg-current animate-pulse align-middle" />
                        )}
                      </div>
                      <div
                        className={`text-[10px] mt-2 text-right ${message.sender === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                          }`}
                      >
                        {message.timestamp.toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </div>
                    </div>
                    {message.sender === 'user' && (
                      <div className="mt-0.5 flex-shrink-0 p-1 bg-primary-foreground/10 text-primary-foreground rounded-lg">
                        <User size={16} />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && !streamingMessageId && (
              <div className="flex justify-start">
                <div className="bg-card border border-border/60 rounded-2xl rounded-bl-none p-4 shadow-sm">
                  <div className="flex space-x-1.5 items-center h-4">
                    <div className="w-2 h-2 bg-muted-foreground/45 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-muted-foreground/45 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-muted-foreground/45 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <div className="border-t border-border/80 p-4 bg-card/40">
            <div className="flex space-x-3">
              <input
                ref={inputRef}
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Napisz pytanie do Asystenta..."
                disabled={isLoading}
                className="flex-1 px-5 py-3.5 bg-background border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary disabled:opacity-60 text-sm placeholder:text-muted-foreground"
              />
              <button
                onClick={isLoading ? handleCancelRequest : handleSendMessage}
                disabled={!inputText.trim() && !isLoading}
                className={`px-5 rounded-xl text-white font-medium text-sm transition-all flex items-center justify-center gap-2 ${isLoading
                  ? 'bg-destructive hover:bg-destructive/90 shadow-glow-accent'
                  : 'bg-primary hover:bg-primary/95 shadow-glow-primary disabled:opacity-50 disabled:shadow-none'
                  }`}
              >
                {isLoading ? (
                  <span>Przerwij</span>
                ) : (
                  <>
                    <span>Wyślij</span>
                    <Send size={16} />
                  </>
                )}
              </button>
            </div>
            <div className="text-[10px] text-muted-foreground text-center mt-2.5">
              Naciśnij Enter, aby wysłać • Shift+Enter dla nowej linii
            </div>
          </div>

        </div>
      </main>

      <Footer />
    </div>
  )
}
