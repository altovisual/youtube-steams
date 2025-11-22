import { cn } from '../../lib/utils'

const variants = {
  primary: 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:shadow-xl hover:scale-[1.02] active:animate-pulse',
  secondary: 'bg-gradient-to-r from-purple-500 to-pink-600 text-white hover:shadow-xl hover:scale-[1.02] active:animate-pulse',
  success: 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg',
}

export default function Button({ 
  children, 
  variant = 'primary', 
  className, 
  disabled,
  ...props 
}) {
  return (
    <button
      className={cn(
        'flex items-center justify-center gap-2',
        'px-6 py-3 rounded-xl',
        'font-semibold text-base',
        'transition-all duration-200',
        'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100',
        variants[variant],
        className
      )}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  )
}
