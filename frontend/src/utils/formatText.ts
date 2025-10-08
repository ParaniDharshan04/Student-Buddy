/**
 * Clean markdown formatting from text
 * Removes *** and # symbols while preserving readability
 */
export const cleanMarkdown = (text: string): string => {
  if (!text) return ''
  
  let cleaned = text
  
  // Remove bold/italic markers (*** or **)
  cleaned = cleaned.replace(/\*\*\*/g, '')
  cleaned = cleaned.replace(/\*\*/g, '')
  cleaned = cleaned.replace(/\*/g, '')
  
  // Remove header markers (#) but keep the text
  cleaned = cleaned.replace(/^#{1,6}\s+/gm, '')
  
  // Remove inline code markers (`)
  cleaned = cleaned.replace(/`/g, '')
  
  // Clean up extra whitespace
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n')
  cleaned = cleaned.trim()
  
  return cleaned
}

/**
 * Format text for better display
 * Converts markdown to plain text with proper spacing
 */
export const formatForDisplay = (text: string): string => {
  if (!text) return ''
  
  let formatted = text
  
  // Convert bold markers to nothing (remove emphasis)
  formatted = formatted.replace(/\*\*\*(.+?)\*\*\*/g, '$1')
  formatted = formatted.replace(/\*\*(.+?)\*\*/g, '$1')
  formatted = formatted.replace(/\*(.+?)\*/g, '$1')
  
  // Convert headers to plain text with line breaks
  formatted = formatted.replace(/^#{1,6}\s+(.+)$/gm, '\n$1\n')
  
  // Remove code markers
  formatted = formatted.replace(/`(.+?)`/g, '$1')
  
  // Clean up spacing
  formatted = formatted.replace(/\n{3,}/g, '\n\n')
  formatted = formatted.trim()
  
  return formatted
}
