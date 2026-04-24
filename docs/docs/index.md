# Ph-Eye

Ph-Eye is a service for hosting AI/NLP models for the purposes of finding PII and PHI in text.

Ph-Eye provides a simple REST API that allows you to send text and receive a list of identified entities. It is built on top of the [GLiNER](https://github.com/urchade/GLiNER) library and uses zero-shot learning to identify various types of entities based on the labels you provide.

Current Version: `1.2.1`

While Ph-Eye can be used standalone, it was designed and created for use with [Phileas](https://github.com/philterd/phileas) and [Philter](https://github.com/philterd/philter) and as such provides tight integration with each.

## Features

- **Zero-shot NER**: Use Ph-Eye to find any type of entity without retraining the model.
- **REST API**: Simple JSON-based API for easy integration.
- **Dockerized**: Easily deployable as a Docker container.
- **Integration**: Works seamlessly with Phileas and Philter.

## License

Ph-Eye is licensed under the Apache License, version 2.0. However, the model(s) used by Ph-Eye may be used under a different license. Please refer to the specific model being used for information about its license.
