import { renderHook, act } from '@testing-library/react'
import { expect, describe, it } from 'vitest'
import { useCounter } from '../../src/hooks/useCounter'

describe('useCounter hook', () => {
    it('should initialize with default value', () => {
        const { result } = renderHook(() => useCounter())

        expect(result.current.count).toBe(0)
    })

    it('should initialize with custom value', () => {
        const { result } = renderHook(() => useCounter(10))

        expect(result.current.count).toBe(10)
    })

    it('should increment the counter', () => {
        const { result } = renderHook(() => useCounter())

        act(() => {
        result.current.increment()
        })

        expect(result.current.count).toBe(1)
    })

    it('should decrement the counter', () => {
        const { result } = renderHook(() => useCounter())

        act(() => {
        result.current.decrement()
        })

        expect(result.current.count).toBe(-1)
    })

    it('should reset the counter', () => {
        const { result } = renderHook(() => useCounter(5))

        act(() => {
        result.current.increment()
        result.current.increment()
        })

        expect(result.current.count).toBe(7)

        act(() => {
        result.current.reset()
        })

        expect(result.current.count).toBe(5)
    })
})