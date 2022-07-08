export const delay = async (timeout: number) => {
    await new Promise(resolve => {
        setTimeout(() => {
            resolve(1)
        }, timeout)
    })
}

export const getNow = (): string => {
    const now = new Date()
    return now.toLocaleString()
}
