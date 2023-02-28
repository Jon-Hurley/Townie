export const buttonBaseStyle = `
    border-2 rounded
    font-medium
    hover:bg-black hover:bg-opacity-5
    focus:outline-none focus:ring-0
    transition duration-150 ease-in-out
`;
export const buttonStyle = `
    p-3 text-md
    ${buttonBaseStyle}
`;

export const redStyle = `
    border-red-500
    text-red-500
`;
export const greenStyle = `
    border-green-500
    text-green-500
`;
export const blueStyle = `
    border-blue-500
    text-blue-500
`;
export const indigoStyle = `
    border-indigo-500
    text-indigo-500
`;
export const grayStyle = `
    border-gray-500
    text-gray-500
`;

export const inputStyle = `
    m-0 w-full p-3 pl-8
    rounded border border-gray-200
    bg-gray-200
    focus:bg-white focus:outline-none
    focus:ring-2 focus:ring-indigo-500
    focus:border-transparent
`;

export const largeTitle = `
    my-4
    text-2xl
    text-center
    font-bold
    text-gray-700
`;

export const hr = "bg-gray-100 h-[2px]";

export const gridItem = `
    p-3 h-[51px] m-0

    border-gray-200 border-2 rounded
    text-gray-900 text-center

    hover:scale-110
    cursor-pointer
`;

export const listItem = `
    mb-2 p-3 w-full

    bg-white text-gray-900
    border-gray-200 border-2 rounded

    flex justify-between items-center

    cursor-pointer
`;