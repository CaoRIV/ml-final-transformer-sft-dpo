-- Keep all content; only adapt heading levels, inline-code wrapping and PDF links.
function Header(el)
  if el.level == 1 then
    return {}
  end
  el.level = el.level - 1
  return el
end

function Code(el)
  -- Schema names must wrap inside narrow table columns, not protrude into margins.
  return pandoc.RawInline('latex', '\\nolinkurl{' .. el.text .. '}')
end

function Link(el)
  if el.target == 'data-plan.md' or el.target == 'proposal.md' then
    el.target = el.target:gsub('%.md$', '.pdf')
  end
  return el
end
