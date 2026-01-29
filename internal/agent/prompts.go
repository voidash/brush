package agent

import (
	"context"
	_ "embed"
	"log/slog"
	"os"
	"path/filepath"

	"github.com/charmbracelet/brush/internal/agent/prompt"
	"github.com/charmbracelet/brush/internal/config"
)

//go:embed templates/coder.md.tpl
var coderPromptTmpl []byte

//go:embed templates/task.md.tpl
var taskPromptTmpl []byte

//go:embed templates/initialize.md.tpl
var initializePromptTmpl []byte

// loadTemplate tries to load a template from the custom templates directory.
// If not found, it returns the embedded template as a fallback.
func loadTemplate(customDir, templateName string, embedded []byte) ([]byte, error) {
	if customDir == "" {
		slog.Debug("Using embedded template", "template", templateName, "source", "embedded")
		return embedded, nil
	}

	customPath := filepath.Join(customDir, templateName)
	content, err := os.ReadFile(customPath)
	if err == nil {
		slog.Info("Loaded custom template", "template", templateName, "path", customPath, "size", len(content))
		return content, nil
	}

	// Fall back to embedded template if custom file not found
	slog.Warn("Custom template not found, using embedded fallback",
		"template", templateName,
		"custom_path", customPath,
		"error", err)
	return embedded, nil
}

func coderPrompt(customDir string, opts ...prompt.Option) (*prompt.Prompt, error) {
	tmpl, err := loadTemplate(customDir, "coder.md.tpl", coderPromptTmpl)
	if err != nil {
		return nil, err
	}
	systemPrompt, err := prompt.NewPrompt("coder", string(tmpl), opts...)
	if err != nil {
		return nil, err
	}
	return systemPrompt, nil
}

func taskPrompt(customDir string, opts ...prompt.Option) (*prompt.Prompt, error) {
	tmpl, err := loadTemplate(customDir, "task.md.tpl", taskPromptTmpl)
	if err != nil {
		return nil, err
	}
	systemPrompt, err := prompt.NewPrompt("task", string(tmpl), opts...)
	if err != nil {
		return nil, err
	}
	return systemPrompt, nil
}

func InitializePrompt(cfg config.Config, customDir string) (string, error) {
	tmpl, err := loadTemplate(customDir, "initialize.md.tpl", initializePromptTmpl)
	if err != nil {
		return "", err
	}
	systemPrompt, err := prompt.NewPrompt("initialize", string(tmpl))
	if err != nil {
		return "", err
	}
	return systemPrompt.Build(context.Background(), "", "", cfg)
}
