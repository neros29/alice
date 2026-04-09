return {
    {
        "bjarneo/aether.nvim",
        name = "aether",
        priority = 1000,
        opts = {
            disable_italics = false,
            colors = {
                -- Monotone shades (base00-base07)
                base00 = "#0e0e11", -- Default background
                base01 = "#9b9bb0", -- Lighter background (status bars)
                base02 = "#0e0e11", -- Selection background
                base03 = "#9b9bb0", -- Comments, invisibles
                base04 = "#faf9fa", -- Dark foreground
                base05 = "#faf9fa", -- Default foreground
                base06 = "#faf9fa", -- Light foreground
                base07 = "#faf9fa", -- Light background

                -- Accent colors (base08-base0F)
                base08 = "#ce7eac", -- Variables, errors, red
                base09 = "#e1b0cd", -- Integers, constants, orange
                base0A = "#d49cdf", -- Classes, types, yellow
                base0B = "#95bbdd", -- Strings, green
                base0C = "#7e9cce", -- Support, regex, cyan
                base0D = "#7b75d6", -- Functions, keywords, blue
                base0E = "#bd86d1", -- Keywords, storage, magenta
                base0F = "#dfafe9", -- Deprecated, brown/yellow
            },
        },
        config = function(_, opts)
            require("aether").setup(opts)
            vim.cmd.colorscheme("aether")

            -- Enable hot reload
            require("aether.hotreload").setup()
        end,
    },
    {
        "LazyVim/LazyVim",
        opts = {
            colorscheme = "aether",
        },
    },
}
