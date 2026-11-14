-- simple-filter.lua
-- 简易版过滤器，安全处理table类型内容

function Div(div)
    -- 打印调试信息
    print("Processing Div with class: " .. table.concat(div.classes, ", "))
    print("Content type: " .. type(div.content))
    
    -- 定义环境映射
    local env_mapping = {
        important = "important",
        renwu = "renwu",
        regular = "regular",
        quoteformat = "quoteformat"
    }
    
    -- 检查每个类名
    for _, class_name in ipairs(div.classes) do
        local env_name = env_mapping[class_name]
        if env_name then
            print("Matched class: " .. class_name .. " -> " .. env_name)
            
            -- 创建结果表
            local result = {}
            
            -- 添加开始环境
            table.insert(result, pandoc.RawBlock('latex', '\\begin{' .. env_name .. '}'))
            
            -- 安全处理内容（无论是什么类型）
            if type(div.content) == "table" then
                -- 如果是table，直接添加所有内容
                for _, item in ipairs(div.content) do
                    table.insert(result, item)
                end
            else
                -- 如果不是table，转换为段落
                table.insert(result, pandoc.Para{pandoc.Str(tostring(div.content))})
            end
            
            -- 添加结束环境
            table.insert(result, pandoc.RawBlock('latex', '\\end{' .. env_name .. '}'))
            
            return result
        end
    end
    
    -- 没有匹配的类，返回原始内容
    return div
end

print("lua filter load success!")